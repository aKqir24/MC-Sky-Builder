using System;
using System.IO;

namespace SkyGenerator
{
    public class Process
    {
        public string inputImage { get; set; }

        public Process(string imagePath)
        {
            inputImage = imagePath;
        }

        public object ProcessSky(
            object newImgObj,
            object fromBytesObj,
            object openImgObj,
            object enhanceColorObj,
            object cropImgObj,
            object resizeImgObj,
            object pasteImgObj,
            bool hasResampling,
            object lanczosResample,
            object antialiasResample,
            string imagePath,
            string tempDir,
            string outExtension,
            int imgRes,
            double edgeBlend,
            double curvature,
            double saturation,
            bool rotateTopBottom,
            object onProgressObj)
        {
            dynamic newImg = newImgObj;
            dynamic fromBytes = fromBytesObj;
            dynamic openImg = openImgObj;
            dynamic enhanceColor = enhanceColorObj;
            dynamic cropImg = cropImgObj;
            dynamic resizeImg = resizeImgObj;
            dynamic pasteImg = pasteImgObj;
            dynamic onProgress = onProgressObj;

            dynamic imgIn = openImg(imagePath);
            imgIn = imgIn.convert("RGB");
            if (saturation != 1.0)
            {
                imgIn = enhanceColor(imgIn, saturation);
            }

            int w = (int)imgIn.width;
            int h = (int)imgIn.height;
            int outputWidth = w;
            int outputHeight = (int)(w * 0.75);

            double edge = w / 4.0;
            int correctPosition = (int)(w / 426.0);
            int blendWidth = (int)(edge * edgeBlend);

            double pv = w > h ? w / 999999.0 : h / 999999.0;
            double currentPercent = 1.0;

            byte[] inPixels = imgIn.tobytes();
            byte[] outPixels = new byte[outputWidth * outputHeight * 3];

            const double pi = Math.PI;

            for (int i = 0; i < outputWidth; i++)
            {
                currentPercent += pv;
                if (onProgress != null) onProgress(currentPercent);

                int face = (int)(i / edge);
                int jStart = face == 2 ? 0 : (int)edge;
                int jEnd = face == 2 ? (int)(edge * 3) : (int)(edge * 2);

                for (int j = jStart; j < jEnd; j++)
                {
                    int face2 = j < edge ? 4 : (j >= 2 * edge ? 5 : face);
                    var (x, y, z) = OutImgToXYZ(i, j, face2, edge);

                    double theta = Math.Atan2(y, x);
                    double phi = Math.Atan2(z, Math.Sqrt(x * x + y * y));

                    double uf = 2 * edge * (theta + pi) / pi;
                    double vf = curvature * edge * (pi / 1.869 - phi) / pi;

                    int ui = (int)Math.Floor(uf), vi = (int)Math.Floor(vf);
                    double mu = uf - ui, nu = vf - vi;

                    int viClamped = Math.Clamp(vi, 0, h - 1);
                    int viNextClamped = Math.Clamp(vi + 1, 0, h - 1);

                    int u1 = (ui % w + w) % w;
                    int u2 = ((ui + 1) % w + w) % w;

                    int idxA = (viClamped * w + u1) * 3;
                    int idxB = (viClamped * w + u2) * 3;
                    int idxC = (viNextClamped * w + u1) * 3;
                    int idxD = (viNextClamped * w + u2) * 3;

                    byte ar = inPixels[idxA], ag = inPixels[idxA + 1], ab = inPixels[idxA + 2];
                    byte br = inPixels[idxB], bg = inPixels[idxB + 1], bb = inPixels[idxB + 2];
                    byte cr = inPixels[idxC], cg = inPixels[idxC + 1], cb = inPixels[idxC + 2];
                    byte dr = inPixels[idxD], dg = inPixels[idxD + 1], db = inPixels[idxD + 2];

                    int red = (int)Math.Clamp(Math.Round(ar * (1 - mu) * (1 - nu) + br * mu * (1 - nu) + cr * (1 - mu) * nu + dr * mu * nu), 0, 255);
                    int green = (int)Math.Clamp(Math.Round(ag * (1 - mu) * (1 - nu) + bg * mu * (1 - nu) + cg * (1 - mu) * nu + dg * mu * nu), 0, 255);
                    int blue = (int)Math.Clamp(Math.Round(ab * (1 - mu) * (1 - nu) + bb * mu * (1 - nu) + cb * (1 - mu) * nu + db * mu * nu), 0, 255);

                    int outIdx = (j * outputWidth + i) * 3;
                    outPixels[outIdx] = (byte)red;
                    outPixels[outIdx + 1] = (byte)green;
                    outPixels[outIdx + 2] = (byte)blue;
                }
            }

            object[] sizeArgs = new object[] { outputWidth, outputHeight };
            dynamic outputImage = fromBytes("RGB", sizeArgs, outPixels);
            outputImage.save(Path.Combine(tempDir, "output_sky.png"));

            string[,] nameMap = {
                { "", "", "Top", "" },
                { "Front", "Right", "Back", "Left" },
                { "", "", "Bottom", "" }
            };

            double cubeSize = outputWidth / 4.0;
            double remainingProgress = (100 - currentPercent) / 12 + 0.01;

            for (int row = 0; row < 3; row++)
            {
                for (int col = 0; col < 4; col++)
                {
                    currentPercent += remainingProgress;
                    if (onProgress != null) onProgress(currentPercent);

                    string faceName = nameMap[row, col];
                    if (!string.IsNullOrEmpty(faceName))
                    {
                        int sx = (int)(cubeSize * col);
                        int sy = (int)(cubeSize * row);
                        int size = (int)cubeSize;

                        object[] cropBox = new object[] { sx, sy, sx + size, sy + size };
                        dynamic cropped = cropImg(outputImage, cropBox);
                        dynamic resample = hasResampling ? lanczosResample : antialiasResample;
                        object[] resSize = new object[] { imgRes, imgRes };
                        cropped = resizeImg(cropped, resSize, resample);

                        string filePath = Path.Combine(tempDir, faceName + ".png");
                        if (File.Exists(filePath)) try { File.Delete(filePath); } catch (IOException) { }
                        cropped.save(filePath);
                    }
                }
            }

            dynamic topImg = openImg(Path.Combine(tempDir, "Top" + outExtension));
            topImg = topImg.convert("RGBA");
            topImg = topImg.rotate(180);

            dynamic frontImg = openImg(Path.Combine(tempDir, "Front" + outExtension));
            frontImg = frontImg.convert("RGBA");

            dynamic bottomImg = openImg(Path.Combine(tempDir, "Bottom" + outExtension));
            bottomImg = bottomImg.convert("RGBA");
            bottomImg = bottomImg.rotate(180);

            int th = (int)topImg.height, tw = (int)topImg.width;
            object[] mrgSize = new object[] { tw, th * 3 };
            object[] mrgColor = new object[] { 0, 0, 0, 0 };
            dynamic mrg = newImg("RGBA", mrgSize, mrgColor);
            pasteImg(mrg, topImg, new object[] { 0, 0 });
            pasteImg(mrg, frontImg, new object[] { 0, th });
            pasteImg(mrg, bottomImg, new object[] { 0, th * 2 });

            object[] leftCrop = new object[] { 0, 0, tw / 2, th * 3 };
            object[] rightCrop = new object[] { tw / 2, 0, tw, th * 3 };
            dynamic left = cropImg(mrg, leftCrop);
            dynamic right = cropImg(mrg, rightCrop);

            dynamic combined = newImg("RGBA", mrgSize, mrgColor);
            pasteImg(combined, left, new object[] { 0, 0 });
            pasteImg(combined, right, new object[] { (int)left.width, 0 });

            if (blendWidth > 0)
            {
                int leftWidth = (int)left.width;
                int rightWidth = (int)right.width;
                int combinedHeight = (int)combined.height;

                byte[] leftPixels = left.tobytes();
                byte[] rightPixels = right.tobytes();
                byte[] combPixels = combined.tobytes();

                for (int y = 0; y < combinedHeight; y++)
                {
                    for (int bw = 0; bw < blendWidth; bw++)
                    {
                        double alpha = blendWidth > 1 ? (double)bw / (blendWidth - 1) : 0;
                        int x1 = Math.Clamp(leftWidth - blendWidth + bw, 0, leftWidth - 1);
                        int x2 = Math.Clamp(blendWidth - 1 - bw, 0, rightWidth - 1);

                        int p1Idx = (y * leftWidth + x1) * 4;
                        int p2Idx = (y * rightWidth + x2) * 4;

                        byte p1r = leftPixels[p1Idx], p1g = leftPixels[p1Idx + 1], p1b = leftPixels[p1Idx + 2], p1a = leftPixels[p1Idx + 3];
                        byte p2r = rightPixels[p2Idx], p2g = rightPixels[p2Idx + 1], p2b = rightPixels[p2Idx + 2], p2a = rightPixels[p2Idx + 3];

                        int destX = leftWidth - blendWidth + correctPosition + bw;
                        if ((uint)destX < (uint)tw)
                        {
                            int r = (int)Math.Clamp(Math.Round((1 - alpha) * p1r + alpha * p2r), 0, 255);
                            int g = (int)Math.Clamp(Math.Round((1 - alpha) * p1g + alpha * p2g), 0, 255);
                            int b = (int)Math.Clamp(Math.Round((1 - alpha) * p1b + alpha * p2b), 0, 255);
                            int a = (int)Math.Clamp(Math.Round((1 - alpha) * p1a + alpha * p2a), 0, 255);

                            int combIdx = (y * tw + destX) * 4;
                            combPixels[combIdx] = (byte)r;
                            combPixels[combIdx + 1] = (byte)g;
                            combPixels[combIdx + 2] = (byte)b;
                            combPixels[combIdx + 3] = (byte)a;
                        }
                    }
                }

                combined = fromBytes("RGBA", mrgSize, combPixels);
            }

            string saveMerged = Path.Combine(tempDir, "combined.png");
            combined.save(saveMerged);

            dynamic mergedImage = openImg(saveMerged);
            mergedImage = mergedImage.convert("RGBA");
            int[] nameIndices = { 4, 2, 5 };
            string[] oldNames = { "Back.png", "Left.png", "Front.png", "Right.png", "Top.png", "Bottom.png" };
            for (int i = 0; i < 3; i++)
            {
                string path = Path.Combine(tempDir, oldNames[nameIndices[i]]);
                if (File.Exists(path)) try { File.Delete(path); } catch (IOException) { }

                object[] mergedCropBox = new object[] { 0, imgRes * i, imgRes, imgRes * (i + 1) };
                dynamic cropped = cropImg(mergedImage, mergedCropBox);
                if (i == 2 || (i == 0 && rotateTopBottom))
                {
                    cropped = cropped.rotate(180);
                }
                cropped.save(path);
            }
            if (File.Exists(saveMerged)) try { File.Delete(saveMerged); } catch (IOException) { }

            int[] indices = { 5, 4, 0, 1, 2, 3 };
            int javaWidth = outputWidth / 4;
            int javaHeight = outputWidth / 4;
            object[] javaCanvasSize = new object[] { javaWidth * 3, javaHeight * 2 };
            object[] javaCanvasColor = new object[] { 0, 0, 0, 0 };
            dynamic canvas = newImg("RGBA", javaCanvasSize, javaCanvasColor);
            for (int i = 0; i < 6; i++)
            {
                int idx = indices[i];
                dynamic imgFace = openImg(Path.Combine(tempDir, oldNames[idx]));
                imgFace = imgFace.convert("RGBA");
                int posX = (i < 3 ? i : i - 3) * javaWidth;
                int posY = i < 3 ? 0 : javaHeight;
                pasteImg(canvas, imgFace, new object[] { posX, posY });
            }

            return canvas;
        }

        private (double x, double y, double z) OutImgToXYZ(int i, int j, int face, double edge)
        {
            double a = 2.0 * i / edge, b = 2.0 * j / edge;
            return face switch
            {
                0 => (-1.0, 1.0 - a, 3.0 - b),
                1 => (a - 3.0, -1.0, 3.0 - b),
                2 => (1.0, a - 5.0, 3.0 - b),
                3 => (7.0 - a, 1.0, 3.0 - b),
                4 => (b - 1.0, a - 5.0, 1.0),
                5 => (5.0 - b, a - 5.0, -1.0),
                _ => (0, 0, 0)
            };
        }

        public static string GetImageFormat(string imagePath)
        {
            return Path.GetExtension(imagePath).TrimStart('.').ToLower();
        }
    }
}

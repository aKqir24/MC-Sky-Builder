using System;
using System.IO;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;

/*

    This Code Was Made By People From Stackoverflow
    I Am To Lazy To Make These Kinds Of Hard Code
    Since I'm Just A Beginer I Don't Know Many Maths.

    Originally it was made in python, I ask AI to
    convert it to C#, with the Image Sharp library
    them tweaked some values to make it suite the
    need of this progra.

*/

namespace SkyGenerator
{
    public class Process
    {
        public string inputImage { get; set; }
        public Image<Rgb24> outputImage { get; set; }
        public Size inputImageSize { get; private set; }
        public Size outputImageSize { get; private set; }

        public Process(string imagePath)
        {
            inputImage = imagePath;
            outputImage = new Image<Rgb24>(Configuration.Default, 1, 1);
            FillBlack(outputImage);
        }

        public void InitializeImages()
        {
            using Image<Rgb24> imgIn = Image.Load<Rgb24>(inputImage);
            inputImageSize = imgIn.Size;
            outputImage = new Image<Rgb24>(Configuration.Default, inputImageSize.Width, (int)(inputImageSize.Width * 0.75));
            FillBlack(outputImage);
            outputImageSize = outputImage.Size;
        }

        private void FillBlack(Image<Rgb24> img) =>
            img.ProcessPixelRows(acc => { for (int y = 0; y < acc.Height; y++) acc.GetRowSpan(y).Clear(); });

        public object[] OutputValues(Size inSize, double edgeBlend = 50.0)
        {
            double edge = inSize.Width / 4.0;
            double pv;
            int correctPosition;
            int blendWidth = (int)(edge * edgeBlend);

            if (inSize.Width >= 3840 || inSize.Height >= 2160)
            {
                pv = 0.010;
                correctPosition = 6;
            }
            else if (inSize.Width >= 2048 || inSize.Height >= 1080)
            {
                pv = 0.0225;
                correctPosition = 4;
            }
            else if (inSize.Width >= 1280 || inSize.Height >= 1080)
            {
                pv = 0.045;
                correctPosition = 3;
            }
            else
            {
                pv = 0.071;
                correctPosition = 2;
            }

            return new object[] { pv, correctPosition, blendWidth };
        }

        public double ConvertBack(double pv, double currentPercent, double curvature = 2.14, Action<double> onProgress = null)
        {
            double edge = inputImageSize.Width / 4.0;
            const double pi = Math.PI;

            using Image<Rgb24> imgIn = Image.Load<Rgb24>(inputImage);
            int w = imgIn.Width, h = imgIn.Height;

            outputImage.ProcessPixelRows(outAcc =>
            {
                for (int i = 0; i < outputImageSize.Width; i++)
                {
                    currentPercent += pv;
                    onProgress?.Invoke(currentPercent);

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

                        Rgb24 a = imgIn[u1, viClamped];
                        Rgb24 b = imgIn[u2, viClamped];
                        Rgb24 c = imgIn[u1, viNextClamped];
                        Rgb24 d = imgIn[u2, viNextClamped];

                        outAcc.GetRowSpan(j)[i] = new Rgb24(
                            (byte)Math.Clamp(Math.Round(a.R * (1 - mu) * (1 - nu) + b.R * mu * (1 - nu) + c.R * (1 - mu) * nu + d.R * mu * nu), 0, 255),
                            (byte)Math.Clamp(Math.Round(a.G * (1 - mu) * (1 - nu) + b.G * mu * (1 - nu) + c.G * (1 - mu) * nu + d.G * mu * nu), 0, 255),
                            (byte)Math.Clamp(Math.Round(a.B * (1 - mu) * (1 - nu) + b.B * mu * (1 - nu) + c.B * (1 - mu) * nu + d.B * mu * nu), 0, 255)
                        );
                    }
                }
            });

            return currentPercent;
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

        public double ExportFaces(int imgRes, string tempDir, double pv, double currentPercent, Action<double> onProgress = null)
        {
            string[,] nameMap = {
                { "", "", "Top", "" },
                { "Front", "Right", "Back", "Left" },
                { "", "", "Bottom", "" }
            };

            double cubeSize = outputImageSize.Width / 4.0;

            for (int row = 0; row < 3; row++)
            {
                for (int col = 0; col < 4; col++)
                {
                    currentPercent += pv;
                    onProgress?.Invoke(currentPercent);

                    string faceName = nameMap[row, col];
                    if (!string.IsNullOrEmpty(faceName))
                    {
                        int sx = (int)(cubeSize * col);
                        int sy = (int)(cubeSize * row);
                        int size = (int)cubeSize;

                        using var cropped = outputImage.Clone(x => x.Crop(new Rectangle(sx, sy, size, size)));
                        cropped.Mutate(x => x.Resize(imgRes, imgRes));

                        string filePath = tempDir + faceName + ".png";
                        if (File.Exists(filePath)) try { File.Delete(filePath); } catch (IOException) { }
                        cropped.Save(filePath);
                    }
                }
            }

            return currentPercent;
        }

        public Image<Rgba32> MergeSkyEdges(int correctPosition, int blendWidth, string tempDir, string outExtension)
        {
            using var top = Image.Load<Rgba32>(Path.Combine(tempDir, "Top" + outExtension));
            top.Mutate(x => x.Rotate(180));
            using var front = Image.Load<Rgba32>(Path.Combine(tempDir, "Front" + outExtension));
            using var bottom = Image.Load<Rgba32>(Path.Combine(tempDir, "Bottom" + outExtension));
            bottom.Mutate(x => x.Rotate(180));

            int h = top.Height, w = top.Width;
            var mrg = new Image<Rgba32>(Configuration.Default, w, h * 3);
            mrg.Mutate(x => { x.DrawImage(top, new Point(0, 0), 1f).DrawImage(front, new Point(0, h), 1f).DrawImage(bottom, new Point(0, h * 2), 1f); });

            using var left = mrg.Clone(x => x.Crop(new Rectangle(0, 0, w / 2, h * 3)));
            using var right = mrg.Clone(x => x.Crop(new Rectangle(w / 2, 0, w / 2, h * 3)));

            var combined = new Image<Rgba32>(Configuration.Default, w, h * 3);
            combined.Mutate(x => x.DrawImage(left, new Point(0, 0), 1f).DrawImage(right, new Point(left.Width, 0), 1f));

            if (blendWidth > 0)
            {
                int leftWidth = left.Width;
                int rightWidth = right.Width;
                combined.ProcessPixelRows(acc =>
                {
                    for (int y = 0; y < acc.Height; y++)
                    {
                        var row = acc.GetRowSpan(y);

                        for (int bw = 0; bw < blendWidth; bw++)
                        {
                            double alpha = (double)bw / (blendWidth - 1);
                            int x1 = Math.Clamp(leftWidth - blendWidth + bw, 0, leftWidth - 1);
                            int x2 = Math.Clamp(blendWidth - 1 - bw, 0, rightWidth - 1);

                            Rgba32 p1 = left[x1, y];
                            Rgba32 p2 = right[x2, y];

                            int destX = leftWidth - blendWidth + correctPosition + bw;

                            if ((uint)destX < (uint)acc.Width)
                            {
                                row[destX] = new Rgba32(
                                    (byte)Math.Clamp(Math.Round((1 - alpha) * p1.R + alpha * p2.R), 0, 255),
                                    (byte)Math.Clamp(Math.Round((1 - alpha) * p1.G + alpha * p2.G), 0, 255),
                                    (byte)Math.Clamp(Math.Round((1 - alpha) * p1.B + alpha * p2.B), 0, 255),
                                    (byte)Math.Clamp(Math.Round((1 - alpha) * p1.A + alpha * p2.A), 0, 255)
                                );
                            }
                        }
                    }
                });
            }
            return combined;
        }

        public Image<Rgba32> MergeJavaSky(string tempDir, string[] oldNames, int width, int height)
        {
            int[] indices = { 5, 4, 0, 1, 2, 3 };
            var canvas = new Image<Rgba32>(Configuration.Default, width * 3, height * 2);
            canvas.Mutate(ctx =>
            {
                for (int i = 0; i < 6; i++)
                {
                    using var img = Image.Load<Rgba32>(Path.Combine(tempDir, oldNames[indices[i]]));
                    ctx.DrawImage(img, new Point((i < 3 ? i : i - 3) * width, i < 3 ? 0 : height), 1f);
                }
            });
            return canvas;
        }

        public void CropMergedImage(string[] oldNames, string mergedPath, int imgRes, string tempDir, bool rotateTopBottom = true)
        {
            using var image = Image.Load<Rgba32>(mergedPath);
            int[] nameIndices = { 4, 2, 5 };
            for (int i = 0; i < 3; i++)
            {
                string path = tempDir + oldNames[nameIndices[i]];
                if (File.Exists(path)) try { File.Delete(path); } catch (IOException) { }

                using var cropped = image.Clone(x => x.Crop(new Rectangle(0, imgRes * i, imgRes, imgRes)));
                if (i == 2 || (i == 0 && rotateTopBottom))
                {
                    cropped.Mutate(x => x.Rotate(180));
                }
                cropped.Save(path);
            }
            if (File.Exists(mergedPath)) try { File.Delete(mergedPath); } catch (IOException) { }
        }

        public void GenerateRoundedPreviewFromStream(string inputPath, Stream outputStream, int radius)
        {
            using var image = Image.Load<Rgba32>(inputPath);

            int previewWidth = 512;
            if (image.Width > previewWidth)
            {
                double scale = (double)previewWidth / image.Width;
                int previewHeight = (int)(image.Height * scale);
                image.Mutate(x => x.Resize(previewWidth, previewHeight));
                radius = (int)(radius * scale);
            }

            int width = image.Width;
            int height = image.Height;

            // Centers of the four circular corners
            float rSq = radius * radius;
            int cx1 = radius;
            int cy1 = radius;
            int cx2 = width - radius;
            int cy2 = height - radius;

            image.ProcessPixelRows(acc =>
            {
                for (int y = 0; y < height; y++)
                {
                    Span<Rgba32> row = acc.GetRowSpan(y);
                    for (int x = 0; x < width; x++)
                    {
                        // Determine which corner region this pixel falls into
                        bool isTop = y < radius;
                        bool isBottom = y >= height - radius;
                        bool isLeft = x < radius;
                        bool isRight = x >= width - radius;

                        if ((isTop || isBottom) && (isLeft || isRight))
                        {
                            // Find the respective corner center
                            int targetCx = isLeft ? cx1 : cx2;
                            int targetCy = isTop ? cy1 : cy2;

                            // Calculate exact distance squared from the circle center
                            // Adding 0.5f samples from the pixel center for smooth anti-aliased look
                            float dx = x - targetCx + 0.5f;
                            float dy = y - targetCy + 0.5f;

                            if ((dx * dx + dy * dy) > rSq)
                            {
                                var p = row[x];
                                row[x] = new Rgba32(p.R, p.G, p.B, 0); // Make transparent
                            }
                        }
                    }
                }
            });

            image.SaveAsPng(outputStream);
        }

        public void SaveOutputImage(string path)
        {
            outputImage.Save(path);
        }

        public void SaveRgbaImage(Image<Rgba32> img, string path)
        {
            img.Save(path);
            img.Dispose();
        }

        public static string GetImageFormat(string imagePath) =>
            Image.Identify(imagePath)?.Metadata.DecodedImageFormat?.Name.ToLower() ?? "unknown";
    }
}

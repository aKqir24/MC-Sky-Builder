using System;
using System.IO;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Sky Generator Initialized.");
    }
}

class Process
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

        int newHeight = (int)(inputImageSize.Width * 3.0 / 4.0);
        outputImage = new Image<Rgb24>(Configuration.Default, inputImageSize.Width, newHeight);
        FillBlack(outputImage);
        outputImageSize = outputImage.Size;
    }

    private void FillBlack(Image<Rgb24> img)
    {
        img.ProcessPixelRows(accessor =>
        {
            for (int y = 0; y < accessor.Height; y++)
            {
                Span<Rgb24> row = accessor.GetRowSpan(y);
                row.Fill(new Rgb24(0, 0, 0));
            }
        });
    }

    public (double pv, int correctPosition, int blendWidth) OutputValues(Size inSize, double edgeBlend = 50.0)
    {
        double edge = inSize.Width / 4.0;
        int blendWidth = (int)(edge * edgeBlend);

        double pv;
        int correctPosition;

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

        return (pv, correctPosition, blendWidth);
    }

    public double ConvertBack(double pv, double currentPercent)
    {
        double edge = inputImageSize.Width / 4.0;
        const double pi = Math.PI;
        double curvature = 1.0;

        using Image<Rgb24> imgIn = Image.Load<Rgb24>(inputImage);

        int inWidth = imgIn.Width;
        int inHeight = imgIn.Height;

        outputImage.ProcessPixelRows(outAccessor =>
        {
            for (int i = 0; i < outputImageSize.Width; i++)
            {
                int face = (int)(i / edge);
                int jStart = (face == 2) ? 0 : (int)edge;
                int jEnd = (face == 2) ? (int)(edge * 3) : (int)(edge * 2);

                for (int j = jStart; j < jEnd; j++)
                {
                    int face2;
                    if (j < edge) face2 = 4;      // top
                    else if (j >= 2 * edge) face2 = 5; // bottom
                    else face2 = face;

                    var (x, y, z) = OutImgToXYZ(i, j, face2, edge);
                    double theta = Math.Atan2(y, x);
                    double r = Math.Sqrt(x * x + y * y);
                    double phi = Math.Atan2(z, r);

                    double uf = 2 * edge * (theta + pi) / pi;
                    double vf = curvature * edge * (pi / 1.869 - phi) / pi;

                    int ui = (int)Math.Floor(uf);
                    int vi = (int)Math.Floor(vf);
                    int u2 = ui + 1;
                    int v2 = vi + 1;

                    double mu = uf - ui;
                    double nu = vf - vi;

                    int uiMod = (ui % inWidth + inWidth) % inWidth;
                    int u2Mod = (u2 % inWidth + inWidth) % inWidth;
                    int viClamped = Math.Clamp(vi, 0, inHeight - 1);
                    int v2Clamped = Math.Clamp(v2, 0, inHeight - 1);

                    Rgb24 a = imgIn[uiMod, viClamped];
                    Rgb24 b = imgIn[u2Mod, viClamped];
                    Rgb24 c = imgIn[uiMod, v2Clamped];
                    Rgb24 d = imgIn[u2Mod, v2Clamped];

                    double red = a.R * (1 - mu) * (1 - nu) + b.R * mu * (1 - nu) + c.R * (1 - mu) * nu + d.R * mu * nu;
                    double green = a.G * (1 - mu) * (1 - nu) + b.G * mu * (1 - nu) + c.G * (1 - mu) * nu + d.G * mu * nu;
                    double blue = a.B * (1 - mu) * (1 - nu) + b.B * mu * (1 - nu) + c.B * (1 - mu) * nu + d.B * mu * nu;

                    Span<Rgb24> outRow = outAccessor.GetRowSpan(j);
                    outRow[i] = new Rgb24(
                        (byte)Math.Clamp(Math.Round(red), 0, 255),
                        (byte)Math.Clamp(Math.Round(green), 0, 255),
                        (byte)Math.Clamp(Math.Round(blue), 0, 255)
                    );
                }
            }
        });

        return currentPercent;
    }

    private (double x, double y, double z) OutImgToXYZ(int i, int j, int face, double edge)
    {
        double a = 2.0 * i / edge;
        double b = 2.0 * j / edge;

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

    public Image<Rgba32> MergeSkyEdges(int correctPosition, int blendWidth, string tempDir, string outExtension)
    {
        using var top = Image.Load<Rgba32>(Path.Combine(tempDir, "Top" + outExtension));
        top.Mutate(x => x.Rotate(180));

        using var front = Image.Load<Rgba32>(Path.Combine(tempDir, "Front" + outExtension));

        using var bottom = Image.Load<Rgba32>(Path.Combine(tempDir, "Bottom" + outExtension));
        bottom.Mutate(x => x.Rotate(180));

        int combinedHeight = top.Height * 3;
        var mrg = new Image<Rgba32>(Configuration.Default, top.Width, combinedHeight);

        mrg.Mutate(x =>
        {
            x.DrawImage(top, new Point(0, 0), 1f);
            x.DrawImage(front, new Point(0, top.Height), 1f);
            x.DrawImage(bottom, new Point(0, top.Height * 2), 1f);
        });

        var left = mrg.Clone(x => x.Crop(new Rectangle(0, 0, top.Width / 2, combinedHeight)));
        var right = mrg.Clone(x => x.Crop(new Rectangle(top.Width / 2, 0, top.Width - (top.Width / 2), combinedHeight)));

        var combinedArr = new Image<Rgba32>(Configuration.Default, top.Width, combinedHeight);
        combinedArr.Mutate(x =>
        {
            x.DrawImage(left, new Point(0, 0), 1f);
            x.DrawImage(right, new Point(left.Width, 0), 1f);
        });

        if (blendWidth > 0)
        {
            int leftWidth = left.Width;
            int rightWidth = right.Width;

            combinedArr.ProcessPixelRows(accessor =>
            {
                for (int y = 0; y < accessor.Height; y++)
                {
                    Span<Rgba32> row = accessor.GetRowSpan(y);

                    for (int bw = 0; bw < blendWidth; bw++)
                    {
                        double alpha = (double)bw / (blendWidth - 1);
                        int x1 = Math.Clamp(leftWidth - blendWidth + bw, 0, leftWidth - 1);
                        int x2 = Math.Clamp(blendWidth - 1 - bw, 0, rightWidth - 1);

                        Rgba32 p1 = left[x1, y];
                        Rgba32 p2 = right[x2, y];

                        byte r = (byte)Math.Clamp(Math.Round((1.0 - alpha) * p1.R + alpha * p2.R), 0, 255);
                        byte g = (byte)Math.Clamp(Math.Round((1.0 - alpha) * p1.G + alpha * p2.G), 0, 255);
                        byte b = (byte)Math.Clamp(Math.Round((1.0 - alpha) * p1.B + alpha * p2.B), 0, 255);
                        byte a = (byte)Math.Clamp(Math.Round((1.0 - alpha) * p1.A + alpha * p2.A), 0, 255);

                        int destX = leftWidth - blendWidth + correctPosition + bw;
                        if (destX >= 0 && destX < accessor.Width)
                        {
                            row[destX] = new Rgba32(r, g, b, a);
                        }
                    }
                }
            });
        }

        left.Dispose();
        right.Dispose();
        mrg.Dispose();

        return combinedArr;
    }

    public Image<Rgba32> MergeJavaSky(string tempDir, string[] oldNames, int width, int height)
    {
        int[] indices = new int[] { 5, 4, 0, 1, 2, 3 };
        var images = new Image<Rgba32>[6];

        for (int i = 0; i < 6; i++)
        {
            images[i] = Image.Load<Rgba32>(Path.Combine(tempDir, oldNames[indices[i]]));
        }

        var canvas = new Image<Rgba32>(Configuration.Default, width * 3, height * 2);
        canvas.Mutate(ctx =>
        {
            for (int i = 0; i < 6; i++)
            {
                int x = (i < 3 ? i : i - 3) * width;
                int y = (i < 3 ? 0 : height);
                ctx.DrawImage(images[i], new Point(x, y), 1f);
            }
        });

        foreach (var img in images)
        {
            img.Dispose();
        }

        return canvas;
    }

    public void CropMergedImage(string[] oldNames, string mergedPath, int imgRes, string tempDir)
    {
        var coords = new Rectangle[]
        {
            new Rectangle(0, 0, imgRes, imgRes),
            new Rectangle(0, imgRes, imgRes, imgRes),
            new Rectangle(0, imgRes * 2, imgRes, imgRes)
        };
        int[] nameIndices = new int[] { 4, 2, 5 };

        using (var image = Image.Load<Rgba32>(mergedPath))
        {
            for (int i = 0; i < 3; i++)
            {
                string path = Path.Combine(tempDir, oldNames[nameIndices[i]]);
                if (File.Exists(path))
                {
                    try { File.Delete(path); } catch (IOException) { }
                }

                using var cropped = image.Clone(x => x.Crop(coords[i]));
                if (i == 0 || i == 2)
                {
                    cropped.Mutate(x => x.Rotate(180));
                }
                cropped.Save(path);
            }
        }

        if (File.Exists(mergedPath))
        {
            try { File.Delete(mergedPath); } catch (IOException) { }
        }
    }
}

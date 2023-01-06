using System;
using System.Security.Cryptography;
using System.Text;
using System.IO;
using System.Linq;

class PHDecrypt
{

    public static void Main(String[] args)
    {

        if (args.Length != 2)
        {
            Console.WriteLine("PHDecrypt: Pokemon HOME save file decryptor");
            Console.WriteLine("Usage: PHDecrypt.exe <infile> <outfile>");
            return;
        }

        if (!File.Exists(args[0])) {
            Console.WriteLine("Input file '" + args[0] + "' cannot be found");
            return;
        }

        byte[] bytes = File.ReadAllBytes(args[0]);
        long totalBytes = bytes.Length;

        byte[] key = Encoding.UTF8.GetBytes("d39UMKKKQ9DtxYFSZ4zHiNpnDxCV6GWj");
        byte[] iv = Encoding.UTF8.GetBytes("Y74QZaTahQg4ATQd");

        RijndaelManaged rijndael = new RijndaelManaged();
        rijndael.Padding = PaddingMode.PKCS7;
        rijndael.Mode = CipherMode.CBC;
        rijndael.BlockSize = 128;
        rijndael.KeySize = 256;

        ICryptoTransform transform = rijndael.CreateDecryptor(key, iv);
        MemoryStream inStream = new MemoryStream(bytes, 0, Math.Min(bytes.Length, 0x410));
        MemoryStream outStream = new MemoryStream();

        CryptoStream stream = new CryptoStream(inStream, transform, CryptoStreamMode.Read);

        byte[] buffer = new byte[0x400];

        while (true)
        {
            int count = stream.Read(buffer, 0, 0x400);

            if (count == 0)
            {
                break;
            }

            outStream.Write(buffer, 0, count);
        }

        int unencryptedOffset = 0x410;

        if (totalBytes > unencryptedOffset)
        {
            outStream.Write(bytes, unencryptedOffset, (int)(totalBytes - unencryptedOffset));
        }

        File.WriteAllBytes(args[1], outStream.ToArray().ToArray());
        Console.WriteLine("Done. Written to: '" + args[1] + "'");

    }

}
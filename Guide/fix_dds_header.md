# `fix_dds_header` Script

## Overview

The `fix_dds_header` script is a Visual Basic .NET (VB.NET) program designed to fix the headers of DDS (DirectDraw Surface) files. Specifically, it ensures that the header of each DDS file starts with the correct bytes, which are `44 44 53 20` (representing "DDS "). The script performs the following tasks:

1. Verifies that `Client.exe` is present in the current directory.
2. Searches for all `.dds` files in the current directory and its subdirectories.
3. Checks if the DDS files have a specific header.
4. Replaces the header with the correct bytes if needed.
5. Saves the modified files.

## Script Explanation

```vb
Sub Main()
    Dim nHeader As Byte() = {&H44, &H44, &H53, &H20} ' DDS header bytes
    Dim iDir As String = ".\\"
    Dim rylClient As System.Collections.ObjectModel.ReadOnlyCollection(Of String) = My.Computer.FileSystem.GetFiles(iDir, FileIO.SearchOption.SearchTopLevelOnly, "Client.exe")
    
    ' Check if Client.exe is present in the directory
    If rylClient.Count <> 1 Then
        Console.WriteLine("Place this tool in your ryl2 directory")
        Console.WriteLine("")
        Console.WriteLine("Hit enter to exit")
        Console.ReadLine()
        Exit Sub
    End If

    Console.WriteLine("Parsing files....")
    
    ' Find all .dds files in the current directory and subdirectories
    Dim files As System.Collections.ObjectModel.ReadOnlyCollection(Of String) = My.Computer.FileSystem.GetFiles(iDir, FileIO.SearchOption.SearchAllSubDirectories, "*.dds")

    Console.WriteLine("Number of found files: " & files.Count)
    Console.WriteLine("")
    Console.WriteLine("Hit enter to continue or Ctrl+C to exit")
    Console.ReadLine()
    
    Dim changedF As Integer = 0
    Console.WriteLine("Editing DDS files... Please wait.")
    
    ' Iterate through each .dds file
    For Each f As String In files
        Try
            Dim bw As IO.FileStream = IO.File.Open(f, IO.FileMode.Open, IO.FileAccess.ReadWrite, IO.FileShare.None)
            Dim header(4) As Byte
            Dim readed As Integer = bw.Read(header, 0, 5)
            
            ' Check if the current header matches the incorrect header
            If readed = 5 Then
                If header(0) = &H0 AndAlso header(1) = &H0 AndAlso header(2) = &H0 AndAlso header(3) = &H0 AndAlso header(4) = &H7C Then
                    Console.WriteLine(f)
                    bw.Seek(0, IO.SeekOrigin.Begin)
                    bw.Write(nHeader, 0, nHeader.Length) ' Write the correct header bytes
                    bw.Flush()
                    changedF += 1
                End If
            End If
            bw.Close()
        Catch ex As Exception
            Console.WriteLine("Error happened: " & ex.Message)
            Console.WriteLine()
            Console.WriteLine("Exiting...")
            GoTo x
        End Try
    Next
    
x:  Console.WriteLine("Edited " & changedF & " files. " & (files.Count - changedF) & " files had already DDS header. Hit enter to exit")
    Console.ReadLine()
End Sub
```
# Script Details

- **Check for `Client.exe`:**

  The script ensures that `Client.exe` is present in the current directory. If not, it prompts the user to place the tool in the correct directory and exits.

- **File Search:**

  It searches for all `.dds` files in the current directory and all subdirectories.

- **Header Check:**

  The script reads the first 5 bytes of each DDS file to check if they match a specific incorrect header (`00 00 00 00 7C`).

- **Header Correction:**

  If the header is incorrect, the script replaces it with the correct header bytes (`44 44 53 20`).

- **Completion Message:**

  After processing, it displays the number of files that were edited and those that already had the correct header.

## Usage

1. Place the `fix_dds_header` script in the same directory as `Client.exe`.
2. Run the script.
3. It will automatically find and correct DDS files as needed.

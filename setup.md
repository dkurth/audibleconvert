Setup: You need to create a file called `activation_bytes.txt`. It should contain an 8-character hex value, like "4ca9bf43".

Everyone's activation bytes string is different. You only have to get it once, but it's a little complicated. These steps (particularly running `rcrack`) only worked for me on Windows:

- Log in to Audible and go to the Library page
- Click the Download link under one of your titles to download an .aax file
- Install ffmpeg if you don't already have it
- Run `ffprobe YourFile.aax` and look for something like this in the output: `[aax] file checksum == a8b6c007ecbc3bfd8d5f57664248d441fbc19f4c`
- Clone this project: `https://github.com/inAudible-NG/tables`
- From the `tables` directory, run `run\rcrack.exe . -h a8b6c007ecbc3bfd8d5f57664248d441fbc19f4c`

Look for something like this:

```
result
----------------------------------------------------------------
a8b6c007ecbc3bfd8d5f57664248d441fbc19f4c  |\xb3\x21\x03  hex:4ca9bf43
```

That hex value (`4ca9bf43` in this example) is your activation bytes. Copy it into a new file called `activation_bytes.txt` in this directory, and you're good to go.

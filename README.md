# audibleconvert

This is a command meant to be used with [dk](https://github.com/dkurth/dk).

## Usage

Once you set up your `activation_bytes.yml` file (see below), `dk audibleconvert something.aax` will create `something.mp3`.

If you have multiple profiles, use `dk audibleconvert profile_name something.aax`.

## One time setup: Get your Activation Bytes

Before you can use this command, you need to create a file called `activation_bytes.yml`. It should contain one or more named profiles, each with an 8-character hex value, like this:

```
[my_main_profile]
abcd1234

[other]
fdef9876
```

The first profile is the default (used if you don't specify a profile when running this command).

Everyone's activation bytes string is different. You only have to get it once, but it's a little complicated. These steps (particularly running `rcrack`) only worked for me on Windows or within an Ubuntu Docker container:

- Log in to Audible and go to the Library page
- Click the Download link under one of your titles to download an .aax file
- Install ffmpeg if you don't already have it
- Run `ffprobe YourFile.aax` and look for something like this in the output: `[aax] file checksum == a8b6c007ecbc3bfd8d5f57664248d441fbc19f4c`
- Clone this project: `https://github.com/dkurth/audibleconvert`
    + This is a fork of `https://github.com/inAudible-NG/tables`
    + The only difference is, I added a Dockerfile that lets you run `rcrack` in a container, since `rcrack` doesn't run on MacOS.
- Build the docker container if needed.
    + `docker build --no-cache -t rainbowcrack .`
- From the `tables` directory, run:
    + `docker run -it --rm -v "$PWD":/work rainbowcrack`
    + Now from within the container, run: `./rcrack . -h a8b6c007ecbc3bfd8d5f57664248d441fbc19f4c`

Look for something like this:

```
result
----------------------------------------------------------------
a8b6c007ecbc3bfd8d5f57664248d441fbc19f4c  |\xb3\x21\x03  hex:4ca9bf43
```

That hex value (`4ca9bf43` in this example) is your activation bytes. Copy it into your `activation_bytes.yml` in this directory, give the profile a name (`my_profile` or whatever) and you're good to go.


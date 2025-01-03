
<div align="center"><img src="res/icon.png" height="200" ></img>
<h1>MC-Sky-Builder</h1>
<d>A Program I Made That, Turns Your Choosen Image Into A Sky Overlay Pack Or Cubemap, And Exports It For Both For Java & Bedrock(Windows 10 Edition) Platforms.</d>
</div>

<h3> Features </h3>
<ol>
    <li> Supports Sky Packing For Java & Bedrock (.mcpack or .zip) </li>
    <li> You Can Overide The Sky Resolution With 'Custom Resolutions' </li> 
    <li> Seperated Java, Bedrock, and Both Sky Output </li>
</ol>

![screen_shot](https://github.com/user-attachments/assets/76a35f6f-4f3d-43c9-b303-d3cb28388ac6)

## Setup
The program was only compiled in windows 10 and may not work in some systems, these the methods to get it running. Also do not forget to install the dependencies when compiling from source.

- **For Windows**
    - Just simply download the zip file from the [releases](https://github.com/aKqir24/MC-Sky-Builder/releases) and double click the `MC_Sky_Builder.exe` to start the program.

- **For Linux**
    - Install `wine` in your linux machine then download the zip file from the [releases](https://github.com/aKqir24/MC-Sky-Builder/releases) and launch it by `wine '/path /to /MC_Sky_Builder.exe'`.

## Compiling
In order for this to work you need `pyhon`, `pillow`, `numpy` and if your in a linux distro you need `wine` installed with the previous dependencies I mentioned installed inside in `wine`.

    
- For `Windows`:
    ```cmd
    git clone https://github.com/aKqir24/MC-Sky-Builder.git
    cd MC-Sky-Builder
    python window.py
    ```

- For `Linux`:

  If don't wanna use wine, just ignore this commands...

    ```bash
    git clone https://github.com/aKqir24/MC-Sky-Builder.git
    cd MC-Sky-Builder
    ./wine-run.sh
    ```
## Usage
1. First Open an image by pressing the open button
2. Setup the Settings like the Output Folder, the sky overlay resolution and more...
3. Wait for it to reach 100%
4. Finally Open the output folder and enjoy

<br>
<div align="center">
<h2>WARNING⚠!!</h2>
<d>Some images might not load or result into a perfect sky overlay, due to the limitaions of my ability to code a better one and of the modules.</d>
</div>

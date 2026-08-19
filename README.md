
<div align="center">
<img height="200" alt="app" src="https://github.com/user-attachments/assets/aa5a7b84-d61c-4de9-b5a6-19a6d605d045"/>
<h1>MC-Sky-Builder</h1>

![Codacy grade](https://img.shields.io/codacy/grade/8b0de239c77f4787830779608186b5fa?style=for-the-badge)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/aKqir24/MC-Sky-Builder/release.yml?branch=main&style=for-the-badge)
![GitHub Release](https://img.shields.io/github/v/release/aKqir24/MC-Sky-Builder?sort=semver&display_name=release&style=for-the-badge&color=%231670FF)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/aKqir24/MC-Sky-Builder/total?style=for-the-badge&color=33C3C1)

<d>A Program I Made That, Turns Your Chosen Image Into A Sky Overlay Pack Or Cubemap, And Exports It For Both For Java & Bedrock(Windows 10 Edition) Platforms.</d>
</div>

<h3> Features </h3>
<ol>
    <li> Supports Sky Packing For Java & Bedrock (.mcpack or .zip) </li>
    <li> You Can Overide The Sky Resolution With 'Custom Resolutions' </li>
    <li> Seperated Java, Bedrock, and Both Sky Output </li>
</ol>

<div align="center"><img width="682" height="298" alt="screenshot" src="https://github.com/user-attachments/assets/a6d36be8-9ef8-4cb2-85d9-023655b177a3" /></div>

## Setup
The program was only compiled in windows 10 and may not work in some systems, just simply download the zip file from the [releases](https://github.com/aKqir24/MC-Sky-Builder/releases) and double click the `MC_Sky_Builder.exe` to start the program.


## Licensing
Recently I replaced the <u>Pillow</u>, with a C# alternative called <u>ImageSharp</u>. The library is free for opensource projects like this, but if you want to make that warning not show during compile, I recomend you to apply for a free license in https://licensing.sixlabors.com/, make a `sixlabors.lic` along with the license ID and put in the root path in this project.

## Compiling
In order for this to work you need `pyhon`, `dotnet10` and all the dependecies are managed by the languages.

```shell
git clone https://github.com/aKqir24/MC-Sky-Builder.git
cd MC-Sky-Builder
bash scripts/build.sh
```

The script is not done yet, I am still figuring out what compiler to use other than the native python one.
For now you can run the code as it is and test it.
```bash
    source src/.venv/bin/activate
    pip install -r requirements.txt
    dotnet build generator
    python3 -m src
```

## Usage
1. First Open an image by pressing the open button
2. Setup the Settings like the Output Folder, the sky overlay resolution and more...
3. Wait for it to reach 100%
4. Finally Open the output folder and enjoy

<br>
<div align="center">
<h2>WARNING⚠!!</h2>
<d>Some images might not load or result into a perfect sky overlay, due to the limitations of my ability to code a better one and of the modules.</d>
</div>

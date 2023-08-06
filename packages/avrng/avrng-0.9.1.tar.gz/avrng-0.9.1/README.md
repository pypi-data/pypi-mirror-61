# AVRNG  / CSRNG - VDSF 2020 submission
An audio-visual random number generator, built for the Vancouver District Science Fair 2020.  
Built with Python 3.7, October 2019 - current.  
This PIP package is a mirror of the project at [the GitHub](https://github.com/kewbish/csrng). This distribution may lag behind development at the GitHub.  

## Applications
The AVRNG works well in a variety of application, mainly for security and surveillance-based solutions. One example use case is in an office, where security cameras can pass footage to the AVRNG and generate keys for the office's encryption algorithms. These keys are *truly random* due to the inherent randomness in sensor data when capturing footage, and to unpredictable compression and time-stamps.  
To find the key, an attacker would have to obtain the exact data source with the same compression and XOR rate, and hash at the exact time and parameters the program would be running at. This security makes the AVRNG a [TRNG](https://en.wikipedia.org/wiki/Hardware_random_number_generator).  
A main inspiration was unique TRNG creations, such as the ones employed by [Cloudflare](https://blog.cloudflare.com/lavarand-in-production-the-nitty-gritty-technical-details/). A great video on the topic was created by [Tom Scott](https://www.youtube.com/watch?v=1cUUfMeOijg).  

## How it works
A video is split into audio and video streams. These streams are cut to smaller intervals.  
For the audio, it's split on the interval specified in running the AVRNG. This smaller .wav file is hashed with [Skein](http://www.skein-hash.info/about), a next-level hash and former SHA3 candidate.  
The video stream is cut with the [scenedetect](https://pypi.org/project/scenedetect/) tool, splitting at every unique scene. This works especially well with security footage (main application) with many pauses or intervals of near-identical footage. These smaller videos are then split into individual JPEGS, due to the JPEG's compression algorithm that will preserve the inherent randomness in the camera's sensor data. These photos then are hashed with Skein, as above.  
These two data streams are intertwined together along with a time component, using XOR and bit addition algorithms. These outputs are written to a file, which can then be used as keys for cryptosecure applications.  

## Installation
### With PIP
This method requires PIP to be installed and set up on your machine.  
Open Terminal, and run `pip install avrng` to install the package.
### With Git / Command Line
This method requires Git to be set up properly and configured on your machine.  
Open Terminal, Command Prompt, or Git Bash (or any terminal app), and run `git clone https://github.com/kewbish/csrng.git` to create a copy of this repo on your local machine.  
You should have a folder with the files. Proceed to installing dependencies.  
### With GitHub.com UI
Navigate to [https://github.com/kewbish/CSRNG](https://github.com/kewbish/CSRNG) and click the green `Clone or download` button. Choose to `Download ZIP`. Navigate to the folder downloaded, and unzip the project files. Proceed to installing dependencies.   
### With GitHub Desktop
This method requires GitHub Desktop.  
Open GitHub Desktop. (Alternatively, click `Clone or download` and select `Open with Desktop`.)  
Click the `Add` dropdown in the top-left, and select `Clone a repository`. Open the `URL` pane, and paste `https://github.com/kewbish/CSRNG` into the `Repository URL` field. Select a local path, and click `Clone`.  
You should now have a copy of the project files. Proceed to installing dependencies.   
### Dependencies
Install the following via pip:
- [Pydub](https://pypi.org/project/pydub/)
- [Pyskein](https://pypi.org/project/pyskein/)
- [Scenedetect](https://pypi.org/project/scenedetect/) (requires [numpy](https://numpy.org), [opencv2](https://github.com/opencv/opencv), and [ffmpeg](https://ffmpeg.org))
Alternatively, run `pip install -r requirements.txt` with the prepackaged requirements file. 

## Documentation
A GUI tool and a CLI are included.  
### GUI Usage
To run the GUI, open Terminal (or similar) and run `python3 main.py` in the project root. Alternatively, run `main.py` in an IDE.  
To use the Tkinter GUI, input your desired values. The defaults are what I've tested to be the most consistent.  
The end button will open a file dialog. Navigate to your desired source .mp4.  
The output file will be generated in the parent directory of the selected video file.  
### CLI Usage
To use the CLI, open Terminal (or similar) and run `python3 hash.py path\to\file.mp4 17 1`.  
The `return_all()` function wraps all the functionality of the AVRNG into one function.  
Its three arguments are as follows:
- path: complete path to source file
- cs: length of individual output number
- ai: interval to read data, in seconds
Sample command - `python hash.py \files\video.mp4 17 1`
This will generate a text file with individual numbers in `videos` directory.  
This format is also used when importing and using the `avrng` pip package.  

## Comparison
The following comparison is between the AVRNG and the inbuilt Python random.randint() function.
Test | AVRNG | Inbuilt Python | Comments
--- | --- | --- | ---
Runs Test | 0.38529 | 0.15147 | AVRNG 2.5 times more random
Entropy / bit | 0.984360 | 0.982485 | AVRNG 0.19% more random
Chi square | 28742.64 | 365.44 | AVRNG 78.65 times more distributed
Arithmetic mean | 0.4265 | 0.4222 | AVRNG closer to target 0.5
Serial correlation | 0.018786 | 0.019704 | AVRNG closer to zero, more unexpected
Speed | 22.47s | 0.03513s | Inbuilt Python 639.5 times more efficient

## License
Released under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).
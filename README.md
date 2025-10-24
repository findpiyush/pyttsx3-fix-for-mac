# pyttsx3 fix for MAC

A small guide and troubleshooting repository for using pyttsx3 on macOS. This repo documents a known KeyError: 'VoiceAge' when using pyttsx3 (NSSpeechSynthesizer driver) on macOS.

link to the repo: https://github.com/nateshmbhat/pyttsx3

## Problem

When using pyttsx3 on macOS u may see this traceback :

KeyError: 'VoiceAge'

This happens when the NSSpeechSynthesizer driver (`nsss.py`) expects the `VoiceAge` attribute to exist in the voice attribute dictionary returned by the system, but the way voices are on macOS, it does not provide it. The pyttsx3 code accesses `attr['VoiceAge']` directly, raising a KeyError.

## Do a fresh install inside a virtual environment

Open a terminal and create/activate a virtualenv (optional but i would strongly advise):

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install required packages:

```bash
pip install pyttsx3
pip install pyobjc==9.0.1
```

Notes:

- Use a virtualenv to avoid editing system site-packages.
- Ensure u install this specific version of pyobjc `pyobjc==9.0.1`

## Locate and Edit `nsss.py`

### Finding the nsss.py file location

First, locate where `nsss.py` is installed. In ur virtual environment, it shld be at:

```bash
# If you're in ur project directory with .venv
cd .venv/lib/python3.11/site-packages/pyttsx3/drivers/
```

Or use the full path if needed:

```bash
cd "/<path/to/your/project>/.venv/lib/python3.11/site-packages/pyttsx3/drivers/"
```

### Backup before editing

backup the file just in case u forget what u chancged:

```bash
cp /<path/to>/nsss.py ~/Desktop/nsss.py
```

### How to open and edit nsss.py

You can use a text editor or IDE. Here's how to do it with nano (command line):

1. Navigate to the drivers directory:

   ```bash
   cd .venv/lib/python3.11/site-packages/pyttsx3/drivers/
   ```

2. Open `nsss.py` with nano:

   ```bash
   nano nsss.py
   ```

3. At line 64 there will be `attr['VoiceAge']`; remove this/comment it out:

   ```python
   # Change the return line:
   def _toVoice(self, attr):
       try:
           lang = attr[ 'VoiceLocaleIdentifier']
       except KeyError:
           lang = attr ['VoiceLanguage']
       return Voice(attr[ 'VoiceIdentifier'], attr[ 'VoiceName'],[lang],attr['VoiceGender'],attr['VoiceAge'])

   # To this:
   def _toVoice(self, attr):
       #...code...
       return Voice(attr[ 'VoiceIdentifier'], attr[ 'VoiceName'],[lang],attr['VoiceGender'])
   ```

4. Save and exit:
   - Press `ctrl + x`
   - Press `y` to confirm
   - Press `return/enter` to save

### Test the fix

After editing, run this test script:

```python
import pyttsx3

engine = pyttsx3.init()

engine.say("This is a test message")
engine.runAndWait()

print("hello")

voices = engine.getProperty('voices')
for voice in voices:
     print("ID:", voice.id)
     print("Name:", voice.name)
     print("Languages:", voice.languages)
     print("Gender:", voice.gender)
     print("Age:", voice.age)
     print("")
```

If successful, you should hear the message and see information about all the voices in ur system (without any KeyError).

## Additional Notes

**Important:** It is strongly advised not to change driver files manually; this is just a simple workaround I found online to get the code working for my project. Consider this a temporary fix rather than a permanent solution.

## References/Sources/Acknowledgements

- [Create a virtual environment](https://youtu.be/GZbeL5AcTgw?si=5K61ZeO40dyDOaJI)
- Issue: https://github.com/nateshmbhat/pyttsx3/issues/1
- Issue: https://github.com/nateshmbhat/pyttsx3/issues/248
- StackOverflow: https://stackoverflow.com/questions/74668118/voiceage-error-while-using-pyttsx3-module-to-add-voice-to-statements/74727956#74727956

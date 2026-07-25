import wave
import struct
import math
import random
import os

os.makedirs('assets', exist_ok=True)

# Generate typing sound (short, high-pitched mechanical clicks)
def generate_typing():
    with wave.open('assets/sfx_typing.wav', 'w') as obj:
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(44100)
        for i in range(44100 // 40): # ~25ms sharp click
            value = int(random.uniform(-15000, 15000) * math.exp(-i / 200))
            data = struct.pack('<h', value)
            obj.writeframesraw(data)

# Generate glitch sound (rapid frequency modulation and noise)
def generate_glitch():
    with wave.open('assets/sfx_glitch.wav', 'w') as obj:
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(44100)
        freq = 400
        for i in range(int(44100 * 1.5)): # 1.5 seconds
            if random.random() < 0.05: # erratic frequency shifts
                freq = random.choice([100, 250, 600, 1200, 2400])
            
            if random.random() < 0.15: # digital static noise bursts
                value = int(random.uniform(-20000, 20000))
            else:
                # harsh square wave for that Watch Dogs synth sound
                value = 12000 if math.sin(2 * math.pi * freq * (i / 44100.0)) > 0 else -12000
            
            # Fade out at the end
            fade = 1.0 if i < 44100 else (1.5 - (i/44100.0))
            data = struct.pack('<h', int(value * fade))
            obj.writeframesraw(data)

generate_typing()
generate_glitch()
print("SFX Generated Successfully in assets/")

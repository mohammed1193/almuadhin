import pygame
import os
from pathlib import Path

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_sound = None
        self.is_playing = False
        self.volume = 0.8
    
    def play(self, file_path, volume=None):
        try:
            if not os.path.exists(file_path):
                print(f"Audio file not found: {file_path}")
                return False
            
            if self.is_playing:
                self.stop()
            
            pygame.mixer.music.load(file_path)
            
            if volume is not None:
                pygame.mixer.music.set_volume(volume / 100.0)
            else:
                pygame.mixer.music.set_volume(self.volume)
            
            pygame.mixer.music.play()
            self.is_playing = True
            self.current_sound = file_path
            return True
            
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    
    def stop(self):
        try:
            if self.is_playing:
                pygame.mixer.music.stop()
                self.is_playing = False
                self.current_sound = None
        except Exception as e:
            print(f"Error stopping audio: {e}")
    
    def pause(self):
        try:
            if self.is_playing:
                pygame.mixer.music.pause()
        except Exception as e:
            print(f"Error pausing audio: {e}")
    
    def resume(self):
        try:
            pygame.mixer.music.unpause()
        except Exception as e:
            print(f"Error resuming audio: {e}")
    
    def set_volume(self, volume):
        self.volume = volume / 100.0
        pygame.mixer.music.set_volume(self.volume)
    
    def is_busy(self):
        return pygame.mixer.music.get_busy()
    
    def get_default_adhan_path(self):
        resources_path = Path(__file__).parent.parent.parent / "resources" / "sounds"
        # البحث عن ملف الأذان (MP3 أو WAV)
        for ext in ['.mp3', '.wav']:
            adhan_file = resources_path / f"default_adhan{ext}"
            if adhan_file.exists() and adhan_file.stat().st_size > 0:
                return str(adhan_file)
        return str(resources_path / "default_adhan.mp3")
    
    def get_default_iqama_path(self):
        resources_path = Path(__file__).parent.parent.parent / "resources" / "sounds"
        # البحث عن ملف الإقامة (MP3 أو WAV)
        for ext in ['.mp3', '.wav']:
            iqama_file = resources_path / f"default_iqama{ext}"
            if iqama_file.exists() and iqama_file.stat().st_size > 0:
                return str(iqama_file)
        return str(resources_path / "default_iqama.mp3")

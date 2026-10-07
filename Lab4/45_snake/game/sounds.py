import math
import struct

import pygame


class Sounds:
    def __init__(self):
        self.enabled = False
        self.sample_rate = 44100
        self.eat_sound = None
        self.game_over_sound = None
        self.channels = 1

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=self.sample_rate,
                    size=-16,
                    channels=1,
                    buffer=512
                )

            mixer_frequency, mixer_format, mixer_channels = pygame.mixer.get_init()
            if mixer_frequency <= 0 or mixer_format != -16:
                return

            self.sample_rate = mixer_frequency
            self.channels = mixer_channels
            self.eat_sound = pygame.mixer.Sound(
                buffer=self._make_tone_sequence(
                    [(520, 0.09), (760, 0.11)],
                    gap=0.015
                )
            )
            self.game_over_sound = pygame.mixer.Sound(
                buffer=self._make_tone_sequence(
                    [(520, 0.13), (390, 0.15), (280, 0.18)],
                    gap=0.02
                )
            )
            self.enabled = True
        except pygame.error:
            self.enabled = False
            self.eat_sound = None
            self.game_over_sound = None

    def _make_tone(self, frequency, duration):
        sample_count = int(self.sample_rate * duration)
        fade_samples = max(1, int(self.sample_rate * 0.015))
        frames = []

        for i in range(sample_count):
            amplitude = 0.25
            if i < fade_samples:
                amplitude *= i / fade_samples
            elif i >= sample_count - fade_samples:
                amplitude *= (sample_count - i) / fade_samples

            value = int(
                32767
                * amplitude
                * math.sin(2 * math.pi * frequency * i / self.sample_rate)
            )
            frames.append(struct.pack("<h", value) * self.channels)

        return b"".join(frames)

    def _make_tone_sequence(self, notes, gap=0.0):
        audio = bytearray()
        gap_samples = int(self.sample_rate * gap)

        for frequency, duration in notes:
            audio.extend(self._make_tone(frequency, duration))
            if gap_samples:
                audio.extend(b"\x00\x00" * gap_samples * self.channels)

        return bytes(audio)

    def play_eat(self):
        if self.enabled and self.eat_sound is not None:
            try:
                self.eat_sound.play()
            except pygame.error:
                pass

    def play_game_over(self):
        if self.enabled and self.game_over_sound is not None:
            try:
                self.game_over_sound.play()
            except pygame.error:
                pass

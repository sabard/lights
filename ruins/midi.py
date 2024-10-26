import pygame
import pygame.midi

class MidiKeyboard():
    def __init__(self):
        try:
            pygame.init()
            pygame.midi.init()

            if pygame.midi.get_count() < 1:
                print('Midi board not found!\n')
                self.midiDevice = None
            else:
                device = PYGAME_MIDI_DEVICE if PYGAME_MIDI_DEVICE is not None else pygame.midi.get_default_input_id()
                self.midiDevice = pygame.midi.Input(device, 100)

        except Exception as e:
            print(e)



def check_midi(mIn):
    if mIn.midiDevice:
        if mIn.midiDevice.poll():
            events = mIn.midiDevice.read(1)
            ev_data = events[0][0]
            button = ev_data[1]
            ev_value = ev_data[2]

            print(events)

            if button == 67:
                if ev_value == 127:
                    return True
            elif button == 64:
                if ev_value == 127:
                    return False

    return None

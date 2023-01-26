from time import sleep

NOTE_TO_MOUSE = {
	(0, 34): "mouseLR", # tuple (channel, buffer[0]): "actionAsString"
	(1, 34): "mouseUD",
	(1, 1): "rightMouse",
	(1, 0): "leftMouse",
}

WHEEL_0_RIGHT = 65
WHEEL_0_LEFT = 63

NOTE_TO_KEY = {
	(4, 17): (Key.W, lambda a : a >= 20),
	(4, 18): (Key.S, lambda a : a >= 20),
	(4, 11): [
		(Key.A, lambda a : a <= 15),
		(Key.D, lambda a : a >= 112),
	],
	(4, 5): (Key.A, lambda a : a < 63),
	(4,76): (Key.A, lambda a : a == 127),
	(4,77): (Key.D, lambda a : a == 127),
	(4, 10): (Key.D, lambda a : a > 64),
	(0, 1): (Key.R, lambda a : a == 127),
	(4, 114): (Key.LeftControl, lambda a : a == 127),
	(4, 105): (Key.D1, lambda a : a == 127),
	(4, 107): (Key.D2, lambda a : a == 127),
	(4, 106): (Key.D3, lambda a : a == 127),
	(4, 85): (Key.D4, lambda a : a == 127),
	(4, 86): (Key.D5, lambda a : a == 127),
	(4, 78): (Key.E, lambda a : a == 127),
	(0, 63): (Key.C, lambda a : a == 127),
	(1, 63): (Key.F, lambda a : a == 127),
	(0, 18): (Key.Tab, lambda a : a == 127),
	(4, 71): (Key.Space, lambda a : a == 127),
	(1, 18): (Key.Escape, lambda a : a == 127),
	(0, 0): (Key.Return, lambda a : a == 127),
	(0,8): (Key.NumberPad1, lambda a : a == 127),
	(0,12): (Key.NumberPad2, lambda a : a == 127),
	(0,11): (Key.NumberPad3, lambda a : a == 127),
	(0,13): (Key.NumberPad4, lambda a : a == 127),
	(0,10): (Key.NumberPad5, lambda a : a == 127),
	(1,8): (Key.NumberPad6, lambda a : a == 127),
	(1,12): (Key.NumberPad7, lambda a : a == 127),
	(1,11): (Key.NumberPad8, lambda a : a == 127),
	(1,13): (Key.NumberPad9, lambda a : a == 127),
	(1,10): (Key.NumberPad0, lambda a : a == 127)
}

NOTE_TO_KEY_UPPIES = {
	(4, 45): Key.E,
}

NOTE_TO_CUE = {
	(4, 70): Key.LeftShift,
	(4, 74): Key.Q
}

def update():
	diagnostics.watch(midi[0].data.channel)
	diagnostics.watch(midi[0].data.status)
	diagnostics.watch(midi[0].data.buffer[0]) # Control Num
	diagnostics.watch(midi[0].data.buffer[1]) # Control Value
	diagnostics.debug("channel:")
	diagnostics.debug(midi[0].data.channel)
	diagnostics.debug("control type:")
	diagnostics.debug(midi[0].data.status)    # Control Type
	diagnostics.debug("control number:")
	diagnostics.debug(midi[0].data.buffer[0])
	diagnostics.debug("control value:")
	diagnostics.debug(midi[0].data.buffer[1])
	diagnostics.debug("")
	action = NOTE_TO_MOUSE.get((midi[0].data.channel, midi[0].data.buffer[0]), "NONE")
	if (action != "NONE"):
		diagnostics.debug(action)
		diagnostics.debug("")
		if (action == "mouseLR"):
			if (midi[0].data.buffer[1] > 65): # If going right
				mouse.deltaX = (midi[0].data.buffer[1] - 65) / 3.2
			else:
				mouse.deltaX = (-65 + midi[0].data.buffer[1]) / 3.2
		elif (action == "mouseUD"):
			if (midi[0].data.buffer[1] > 65): # If going right
				mouse.deltaY = (midi[0].data.buffer[1] - 65) / -3.2
			else:
				mouse.deltaY = (-65 + midi[0].data.buffer[1]) / -3.2
		if (action == "leftMouse"):
			mouse.leftButton = midi[0].data.buffer[1] == 127
		elif (action == "rightMouse"):
			mouse.rightButton = midi[0].data.buffer[1] == 127
	else:
		for key, value in NOTE_TO_KEY.iteritems():
			if isinstance(value, list):
				if (key == (midi[0].data.channel, midi[0].data.buffer[0])):
					for t in value:
						keyboard.setKey(t[0], t[1](midi[0].data.buffer[1]))
			else:
				if (key == (midi[0].data.channel, midi[0].data.buffer[0])):
					keyboard.setKey(value[0], value[1](midi[0].data.buffer[1]))
		action = NOTE_TO_KEY_UPPIES.get((midi[0].data.channel, midi[0].data.buffer[0]), "NONE")
		if (action != "NONE"):
			keyboard.setKey(action, True)
			sleep(0.01)
			keyboard.setKey(action, False)
		action = NOTE_TO_CUE.get((midi[0].data.channel, midi[0].data.buffer[0]), "NONE")
		if (action != "NONE"):
			if (midi[0].data.buffer[1] == 127):
				if (keyboard.getKeyDown(action)):
					keyboard.setKey(action, False)
				else:
					keyboard.setKey(action, True)
	

if starting:
	midi[0].update += update

if keyboard.getKeyDown(Key.Grave): 
	mouse.deltaX = 0
	mouse.deltaY = 0
	keyboard.setKeyUp(Key.W)
	exit()	
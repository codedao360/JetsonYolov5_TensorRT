import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

# Create a new pipeline
pipeline = Gst.Pipeline()

# Create a file source to read the Ogg Vorbis file
filesrc = Gst.ElementFactory.make('filesrc', 'filesrc')
filesrc.set_property('location', 'sine.ogg')

# Create an Ogg demuxer
oggdemux = Gst.ElementFactory.make('oggdemux', 'oggdemux')

# Create a Vorbis decoder
vorbisdec = Gst.ElementFactory.make('vorbisdec', 'vorbisdec')

# Create an audioconvert element
audioconvert = Gst.ElementFactory.make('audioconvert', 'audioconvert')

# Create an audioresample element
audioresample = Gst.ElementFactory.make('audioresample', 'audioresample')

# Create a pulsesink to play the audio
pulsesink = Gst.ElementFactory.make('pulsesink', 'pulsesink')

# Add the elements to the pipeline
pipeline.add(filesrc)
pipeline.add(oggdemux)
pipeline.add(vorbisdec)
pipeline.add(audioconvert)
pipeline.add(audioresample)
pipeline.add(pulsesink)

# Link the elements together
filesrc.link(oggdemux)
oggdemux.connect('pad-added', on_demux_pad_added)
vorbisdec.link(audioconvert)
audioconvert.link(audioresample)
audioresample.link(pulsesink)

# Set the pipeline to play in real-time mode
pipeline.set_state(Gst.State.PAUSED)
pipeline.get_state(Gst.CLOCK_TIME_NONE)

# Create a GLib main loop to run the pipeline
loop = GLib.MainLoop()

# Start playing the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Run the GLib main loop
try:
    loop.run()
except KeyboardInterrupt:
    pass

# Stop playing the pipeline
pipeline.set_state(Gst.State.NULL)

def on_demux_pad_added(element, pad):
    # Get the name of the pad's parent element
    parent_name = pad.get_parent_element().get_name()

    # If the parent element is a Vorbis decoder, link the pad to it
    if parent_name == 'vorbisdec':
        pad.link(parent.get_static_pad('sink'))
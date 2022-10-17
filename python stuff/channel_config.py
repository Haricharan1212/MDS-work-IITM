import canlib
import canlib.canlib as clb

def setUpChannel(channel=0, openFlags=clb.Open.ACCEPT_VIRTUAL, outputControl=clb.Driver.NORMAL):
    ch = clb.openChannel(channel, openFlags)
    print("Using channel: %s, EAN: %s" % (clb.ChannelData(channel).channel_name, clb.ChannelData(channel).card_upc_no))

    ch.setBusOutputControl(outputControl)
    ch.busOn()
    return ch

def tearDownChannel(ch):
    ch.busOff()
    ch.close()

def start_channel():
    # Printing number of channels
    num_channels = clb.getNumberOfChannels()
    print(f"Found {num_channels} channels")

    for ch in range(num_channels):
        chd = clb.ChannelData(ch)
        print(f"{ch}. {chd.channel_name} ({chd.card_upc_no} / {chd.card_serial_no})")

    for dev in canlib.connected_devices():
        print(dev.probe_info())    
        
    print("canlib version:", clb.dllversion())
    ch = setUpChannel(channel=0)
    
    return ch
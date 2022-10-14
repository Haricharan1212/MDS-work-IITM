# from canlib import connected_devices, Frame, canlib
# from canlib.canlib import getNumberOfChannels, ChannelData

import canlib
import canlib.canlib as clb

num_channels = clb.getNumberOfChannels()
print(f"Found {num_channels} channels")
for ch in range(num_channels):
    chd = clb.ChannelData(ch)
    print(f"{ch}. {chd.channel_name} ({chd.card_upc_no} / {chd.card_serial_no})")


for dev in canlib.connected_devices():
    print(dev.probe_info())
    
    
def setUpChannel(channel=0,
                 openFlags=clb.Open.ACCEPT_VIRTUAL,
                 outputControl=clb.Driver.NORMAL):
    ch = clb.openChannel(channel, openFlags)
    print("Using channel: %s, EAN: %s" % (clb.ChannelData(channel).channel_name,
                                          clb.ChannelData(channel).card_upc_no))
    ch.setBusOutputControl(outputControl)
    # Specifying a bus speed of 250 kbit/s. See documentation
    # for more informationon how to set bus parameters.
    # params = clb.busparams.BusParamsTq(
    #     tq=8,
    #     phase1=2,
    #     phase2=2,
    #     sjw=1,
    #     prescaler=40,
    #     prop=3
    # )
    # ch.set_bus_params_tq(params)
    ch.busOn()
    return ch

def tearDownChannel(ch):
    ch.busOff()
    ch.close()


print("canlib version:", clb.dllversion())
ch0 = setUpChannel(channel=0)
ch1 = setUpChannel(channel=1)
frame = canlib.Frame(
    id_=100,
    data=[1, 2, 3, 4],
    flags=clb.MessageFlag.EXT
)
ch1.write(frame)
while True:
    try:
        frame = ch0.read()
        print(frame)
        break
    except clb.canNoMsg:
        pass
    except clb.canError as ex:
        print(ex)
tearDownChannel(ch0)
tearDownChannel(ch1)
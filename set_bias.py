# set_bias.py Converts desired bias voltage to DAC values and sends it to appropriate AFE
#Uses the new SPI slave firmware. Python 3.

import DaphneInterface as ivtools
import argparse

def main(ep,afe,v,run_type):

    afe = int(afe)
    v = float(v)

    device = ivtools.daphne(f"10.73.137.{ep}")

    def DAC_for_V(afe, v):
        if afe==0:
            return abs(round((v-0.053)/0.0394))
        elif afe==1:
            return abs(round((v-0.0447)/0.0391))
        elif afe==2:
            return abs(round((v-0.00945)/0.0392))
        elif afe==3:
            return abs(round((v+0.371)/0.0391))
        elif afe==4:
            return abs(round((v-0.00328)/0.0391))
        else:
            raise ValueError("We only have AFE's 0-4!")
    if run_type == 'warm':
        vlimit = 53
    elif run_type == 'cold':
        vlimit = 47
    else:
        raise Exception('run_type not recognized. warm or cold are only options')
    if v==0:
        dac = 0
    elif v > vlimit:
        raise Exception(f'Cannot set bias higher than {vlimit}')
    else:
        dac = DAC_for_V(afe, v)
    
    print('WR VBIASCTRL V 4095')
    response_data = device.command('WR VBIASCTRL V 4095')
    print(response_data)

    CmdString = f"WR AFE {afe} BIASSET V {dac}"
    print(CmdString)

    #send command, read response
    response_data = device.command(CmdString)
    print(response_data)
    
    print('RD VM ALL')
    print(device.command('RD VM ALL'))

    device.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DAPHNE command interpreter')
    parser.add_argument('--ep', required=True, help='DAPHNE IP endpoint, e.g. 110')
    parser.add_argument('--afe', required=True, help='Which AFE are we setting bias for? Number 0-4')
    parser.add_argument('--v', required=True, help='What bias voltage do you want? Positive number')
    parser.add_argument('--run_type', required=True, help='Run type. Choose warm for warm test and cold for cold test.')
    args = parser.parse_args()
    main(args.ep,args.afe,args.v, args.run_type)

import argparse
from math import ceil


file_header = """RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
  530756       0       4
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      80       1
Inst User L.C. Date Time
D2B puentePUEN28-Jan-17 00:56:33
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      80       1
Title                                                                   Scantype
LiCoPO4 Cmcm 20K                                                        2theta
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
      31       4
   nvers   ntype   kctrl   manip   nbang   nkmes  npdone   jcode   ipara   ianal
   imode    itgv  iregul   ivolt    naxe npstart  ilast1     isa  flgkif      ih
      ik   nbsqs  nb_det  nbdata icdesc1 icdesc2 icdesc3 icdesc4 icdesc5 icdesc6
 icdesc7
       4       2       4       1       1      25      25       0       1       0
       0       0       0       0       2       0       0       0       0       0
       0       0       1   16384       1       0       0       0       0       0
       0
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
      50      10
        H (Hmin)        K (Kmin)        L (Lmin)             phi             chi
           omega  2theta (gamma)             psi         ub(1 1)         ub(1 2)
         ub(1 3)         ub(2 1)         ub(2 2)         ub(2 3)         ub(3 1)
         ub(3 2)         ub(3 3)      wavelength  dmonochromator       danalyser
          energy            Hmax            Kmax            Lmax          DeltaH
          DeltaK          DeltaL     Deltaenergy         Ki (Kf)       Ddetector
            xoff            zoff                            yoff        attenuat
      scan start       scan step      scan width          preset    add.bkg.step
   add.bkg.width  add.bkg.preset  couplingfactor         (spare)         (spare)
       Temp-s.pt      Temp-Regul     Temp-sample       Voltmeter       Mag.field
  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
  0.00000000e+00  1.48100006e+02  0.00000000e+00  1.00000000e+00  0.00000000e+00
  0.00000000e+00  0.00000000e+00  1.00000000e+00  0.00000000e+00  0.00000000e+00
  0.00000000e+00  1.00000000e+00  1.60000002e+00  0.00000000e+00  0.00000000e+00
  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
  1.47500000e+02  5.00000007e-02  1.20000005e+00  1.11000000e+06  0.00000000e+00
  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
  2.00000000e+01  2.00000000e+01  2.00119991e+01  0.00000000e+00  0.00000000e+00
"""

shot_header = """SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
       1      24      25  530756       0       1
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
       4       1
            time         monitor       Total Cou     anglesx1000
  7.91410000e+04  1.11000000e+06  1.02520000e+05  {:.8e}
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"""


def get_numbers_every_10(numbers):
    for start in range(0, len(numbers), 10):
        pixels = numbers[start:start + 10]
        yield pixels


def write_shot(fd, numbers):
    fd.write("   16384       0")
    fd.write('\n')
    for group_of_ten in get_numbers_every_10(numbers):
        format_string = "{: >8}"*len(group_of_ten)
        fd.write(format_string.format(*group_of_ten))
        fd.write('\n')


def generate_2d_gradient_pattern(fd, initial_angle, angle_separation):
    angle = initial_angle

    fd.write(file_header)
    for shot in range(25):
        angle += angle_separation
        fd.write(shot_header.format(angle))
        fd.write('\n')
        write_shot(fd, [str(i*shot) for i in range(128)]*60+[str(0)]*128*8+[str(i*shot) for i in range(128)]*60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_angle", help="Initial angle in degrees")
    parser.add_argument("angle_separation", help="Angle separation in degrees")
    parser.add_argument("initial_file_number", help="Initial number for file names")
    parser.add_argument("number_of_shots", help="Number of shots")

    args = parser.parse_args()

    angle_separation = float(args.angle_separation)*1000
    initial_angle = float(args.initial_angle)*1000 - (angle_separation/2.0)
    number_of_files = ceil(int(args.number_of_shots)/25)

    for file_index in range(0, number_of_files):
        file_number = int(args.initial_file_number) + file_index
        with open(str(file_number), 'w') as output:
            generate_2d_gradient_pattern(output, initial_angle, angle_separation)

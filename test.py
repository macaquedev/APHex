import hex_ik
import APHex

h = APHex.APHex(APHex.MG996R)

print(h.shift_lean_calculation(0, 0, 0, 0, 0, 0))
print(hex_ik.shift_lean(0, 0, 0, 0, 0, 0, h.body_side_length, h.foot_length, h.leg_length, h.hip_length))
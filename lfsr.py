from sk_dsp_comm.sigsys import lfsr_seq

# Порождаем последовательность из 20 бит
seq = lfsr_seq(m=9, taps=[9, 7, 3], state=333, N=20)

print(seq)


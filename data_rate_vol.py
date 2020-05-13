def KMGT_Bytes(B):
#-----------------------------------------------------------
# B = data volume or rate in Bytes
# XB = data volume or rate in K/M/G/TBytes
# Unit = KB, MB, GB, TB

    Unit='B' ; XB=B
    k=1024.

    if B >= k and B < k**2:
        XB=B/k ; Unit='KB'

    if B >= k**2 and B < k**3:
        XB=B/k**2 ; Unit='MB'

    if B >= k**3 and B < k**4:
        XB=B/k**3 ; Unit='GB'

    if B >= k**4:
        XB=B/k**4 ; Unit='TB'

    return XB,Unit

def data_rate_vol(Nma=96,Nch=64,dt=1,Df=75,Nb=1,Tobs=3600,mode="BF",Sum=False):
    """
    IDL original version v1, PZ, 20190319
    PYTHON transcript v1, JG, 20200509

    Computes and displays NenuFAR data rates and volumes

    INPUTS
    Nma  = number of Mini-Arrays involved
    Nch  = number of channels / 195.3125 kHz subband
    dt   = integration time of spectra / of visibility sets (sec)
    Df   = total bandwidth (MHz)
    Nb   = N bytes of raw data samples (1 = 8 bits, 2 = 16 bits)
    Tobs = total observation time (sec)

    KEYWORDS
    mode = "BF"  => Beamformer mode	(uses Nch, dt, Df)
           "IM"  => Imager mode		(uses Nma, Nch, dt, Df)
           "WF"  => Waveform mode	(uses Nma)
           "TB"  => Transient Buffer mode (uses Nma, Nb)

    Sum  = 1 line SUMMARY

    OUTPUTS
    D_tot = rate (bytes/sec)
    V_tot = volume (bytes)
    """


    Nsb=min(round(Df/0.1953125),768)

    # BF : 4 float (XX,YY, Re&Im(XY)) per channel per time step
    D_bf_sb=4.*4.*Nch/dt ;  D_bf=D_bf_sb*Nsb ; D_bf_n = D_bf/2  # 2 UnDySPuTeD nodes

    # IM : 4 complex (2x2 correlation matrix) per channel per baseline (+ Auto)
    D_im_sb = 8.*4.*Nch*(Nma*(Nma-1)*1./2+Nma)/dt ; D_im = D_im_sb*Nsb ; D_im_n = D_im/4   # 4 correlator nodes

    # WF : 4 raw values (Re&Im(X), Re&Im(Y)) of 1 or 2 bytes per sample, 195312.5 samples / sec / subband
    D_wf_sb = 4.*Nb*195312.5			; D_wf = D_wf_sb*Nsb	  	   ; D_wf_n = D_wf/2      # 2 UnDySPuTeD nodes

    # TB : 4 raw values (Re&Im(X), Re&Im(Y)) of 1 or 2 bytes per sample, at 200 MHz, per MA
    D_tb_sb = 0.					    ; D_tb = 4.*Nb*2.e8*Nma	       ;  D_tb_n = D_tb		# 1 Waveform node NB0

    if mode == "BF":
        D_sb=D_bf_sb ; D_tot=D_bf ; D_n=D_bf_n ; IM=0 ; WF=0 ; TB=0
    elif mode == "IM":
        D_sb=D_im_sb ; D_tot=D_im ; D_n=D_im_n ; WF=0 ; BF=0 ; WF=0 ; TB=0
    elif mode == "WF":
        D_sb=D_wf_sb ; D_tot=D_wf ; D_n=D_wf_n ; BF=0 ; IM=0 ; TB=0
    elif mode == "TB":
        D_sb=D_tb_sb ; D_tot=D_tb ; D_n=D_tb_n ; BF=0 ; IM=0 ; WF=0
    elif mode == None:
        print("Choose a mode=BF or IM or WF or NB")

    # data rates / sec : /sb, total, /node
    out=''
    XD_sb,U_sb=KMGT_Bytes(D_sb)
    if not(Sum) and mode!="WF":
        out=out+'Rate=  %8.1f %s/s/SB\n'%(XD_sb,U_sb)

    XD_tot, U_tot=KMGT_Bytes(D_tot)
    if not(Sum):
        out=out+'Rate=  %8.1f %s/s\n'%(XD_tot,U_tot)

    XD_n, U_n=KMGT_Bytes(D_n)
    if not(Sum):
        out=out+'Rate=  %8.1f %s/s/node\n'%(XD_n,U_n)


    # data volumes total for Tobs

    V_tot = D_tot*Tobs
    XV_tot, UV_tot=KMGT_Bytes(V_tot)
    if not(Sum):
        out=out+'Volume= %8.1f  %s in %7.0f sec\n'%(XV_tot,UV_tot,Tobs)

    if Sum:
        print("%d MA %d ch/SB %7.3f sec %5.1f MHz %6.0f sec :\n Rate = %6.1f %s /s/SB %6.1f %s /s %6.1f %s /s/node :\n Volume = %6.1f %s)"%(Nma,Nch,dt,Df,Tobs, XD_sb,U_sb,XD_tot,U_tot,XD_n,U_n,XV_tot,UV_tot))
  #format='(i3," MA ",i3," ch/SB ",f7.3," sec ",f5.1," MHz ",f6.0," sec : Rate =",f6.1,1x,a2,"/s/SB ",f6.1,1x,a2,"/s ",f6.1,1x,a2,"/s/node : Volume =",f6.1,1x,a2)'
        out="%d MA %d ch/SB %7.3f sec %5.1f MHz %6.0f sec :\nRate = %6.1f %s /s/SB %6.1f %s /s %6.1f %s /s/node :\nVolume = %6.1f %s\n)"%(Nma,Nch,dt,Df,Tobs, XD_sb,U_sb,XD_tot,U_tot,XD_n,U_n,XV_tot,UV_tot)


    return out
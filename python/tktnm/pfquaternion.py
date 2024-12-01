# -*- coding: utf-8 -*-
'''
quaternionの操作を行う関数群

See Copyright(LICENSE.txt) for the status of this software.
 
Author: Takeharu TANIMURA <tanie@kk.iij4u.or.jp>
'''

import math

from . import pffloat1
from . import pffloat4
from . import pfvector


def sandwich(inQA, inQB) :
  '''
  sandwich(qtA, qtB) -> qtA * qtB * qtA^-1 
  '''
  return multiplyInverse(multiply(inQA, inQB), inQA)

def sandwichInverse(inQA, inQB) :
  '''
  sandwichInverse(qtA, qtB) -> qtA^-1 * qtB * qtA 
  '''
  return multiply(inverseMultiply(inQA, inQB), inQA)

def identity() : 
  '''
  identity() : [0,0,0,1]
  '''
  return list([0.0,0.0,0.0,1.0])

def multiply(inQA, inQB) :
  '''
  multiply(qtA, qtB) -> qtA * qtB
  '''
  # Y * z + X * w + W * x - Z * y
  # W * y + Z * x + Y * w - X * z
  # Z * w + W * z + X * y - Y * x
  # X * x + Y * y + Z * z - W * w

  # X * x
  # Y * z
  # Z * w
  # W * y
  bXZWY = pffloat4.swizzleXZWY(inQB)
  tmp = pffloat4.mul(inQA, bXZWY)

  # Y * z + X * w
  # X * x + Y * y
  # W * y + Z * x
  # Z * w + W * z
  bWYXZ = pffloat4.swizzleWYXZ(inQB)
  tmp = pffloat4.madd(inQA, bWYXZ, pffloat4.swizzleYXWZ(tmp))

  # Y * z + X * w + W * x
  # X * x + Y * y + Z * z
  # W * y + Z * x + Y * w
  # Z * w + W * z + X * y
  aWZYX = pffloat4.swizzleWZYX(inQA)
  tmp = pffloat4.madd(aWZYX, bXZWY, tmp)

  # Y * z + X * w + W * x - Z * y
  # W * y + Z * x + Y * w - X * z
  # Z * w + W * z + X * y - Y * x
  # X * x + Y * y + Z * z - W * w
  aZXYW = pffloat4.swizzleZXYW(inQA)
  bYZXW = pffloat4.swizzleYZXW(inQB)
  tmp = pffloat4.nmsub(aZXYW, bYZXW, pffloat4.swizzleXZWY(tmp))

  #  Y * z + X * w + W * x - Z * y
  #  W * y + Z * x + Y * w - X * z
  #  Z * w + W * z + X * y - Y * x
  # -X * x - Y * y - Z * z + W * w
  return pffloat4.copyW(tmp, pffloat4.neg(tmp))

def rotateX(inQ, inDeg) : 
  '''
  rotateX(q, deg) : rotate Axis X quaterion
  '''
  return multiply(inQ, fromAxisDeg(pffloat4.axisX(), inDeg))
def rotateY(inQ, inDeg) : 
  '''
  rotateY(q, deg) : rotate Axis Y quaterion
  '''
  return multiply(inQ, fromAxisDeg(pffloat4.axisY(), inDeg))
def rotateZ(inQ, inDeg) : 
  '''
  rotateZ(q, deg) : rotate Axis Z quaterion
  '''
  return multiply(inQ, fromAxisDeg(pffloat4.axisZ(), inDeg))

def inverseMultiply(inQA, inQB) :
  '''
  inverseMultiply(qtA, qtB) -> qtA^-1 * qtB
  '''
  # - Y * z - X * w + W * x + Z * y
  # - Z * x - Y * w + W * y + X * z
  # - X * y - Z * w + W * z + Y * x
  # - W * w - W * w + W * w + W * w + X * x + Y * y + Z * z + W * w 

  # + X * x + Y * y + Z * z + W * w
  tmp = pffloat4.setW(pffloat4.zero(), pffloat4.dot4(inQA, inQB))

  # + Z * y
  # + X * z
  # + Y * x
  # + W * w + X * x + Y * y + Z * z + W * w 
  aZXYW = pffloat4.swizzleZXYW(inQA)
  bYZXW = pffloat4.swizzleYZXW(inQB)
  tmp = pffloat4.madd(aZXYW, bYZXW, tmp)

  # + W * x + Z * y
  # + W * y + X * z
  # + W * z + Y * x
  # + W * w + W * w + X * x + Y * y + Z * z + W * w 
  tmp = pffloat4.madd(pffloat4.replicateW(inQA), inQB, tmp)

  # - X * w + W * x + Z * y
  # - Y * w + W * y + X * z
  # - Z * w + W * z + Y * x
  # - W * w + W * w + W * w + X * x + Y * y + Z * z + W * w 
  tmp = pffloat4.nmsub(inQA, pffloat4.replicateW(inQB), tmp)

  # - Y * z - X * w + W * x + Z * y
  # - Z * x - Y * w + W * y + X * z
  # - X * y - Z * w + W * z + Y * x
  # - W * w - W * w + W * w + W * w + X * x + Y * y + Z * z + W * w 
  aYZXW = pffloat4.swizzleYZXW(inQA)
  bZXYW = pffloat4.swizzleZXYW(inQB)
  return pffloat4.nmsub(aYZXW, bZXYW, tmp)

def multiplyInverse(inQA, inQB) :
  '''
  multiplyInverse(qtA, qtB) -> qtA * qtB^-1
  '''
  # - Y * z + X * w - W * x + Z * y
  # - Z * x + Y * w - W * y + X * z
  # - X * y + Z * w - W * z + Y * x
  # - W * w + W * w - W * w + W * w + X * x + Y * y + Z * z + W * w 

  # + X * x + Y * y + Z * z + W * w
  tmp = pffloat4.setW(pffloat4.zero(), pffloat4.dot4(inQA, inQB))

  # + Z * y
  # + X * z
  # + Y * x
  # + W * w + X * x + Y * y + Z * z + W * w 
  aZXYW = pffloat4.swizzleZXYW(inQA)
  bYZXW = pffloat4.swizzleYZXW(inQB)
  tmp = pffloat4.madd(aZXYW, bYZXW, tmp)

  # - W * x + Z * y
  # - W * y + X * z
  # - W * z + Y * x
  # - W * w + W * w + X * x + Y * y + Z * z + W * w 
  tmp = pffloat4.nmsub(pffloat4.replicateW(inQA), inQB, tmp)

  # + X * w - W * x + Z * y
  # + Y * w - W * y + X * z
  # + Z * w - W * z + Y * x
  # + W * w - W * w + W * w + X * x + Y * y + Z * z + W * w 
  tmp = pffloat4.madd(inQA, pffloat4.replicateW(inQB), tmp)

  # - Y * z + X * w - W * x + Z * y
  # - Z * x + Y * w - W * y + X * z
  # - X * y + Z * w - W * z + Y * x
  # - W * w + W * w - W * w + W * w + X * x + Y * y + Z * z + W * w 
  aYZXW = pffloat4.swizzleYZXW(inQA)
  bZXYW = pffloat4.swizzleZXYW(inQB)
  return pffloat4.nmsub(aYZXW, bZXYW, tmp)


def axisX(inQ) :
  '''
  axisX(q) -> [x,y,z,0]
  '''
  # 1 - 2 ( y * y + z * z )
  #     2 ( x * y + z * w )
  #     2 ( z * x - y * w )
  x = pffloat4.getX(inQ)
  y = pffloat4.getY(inQ)
  z = pffloat4.getZ(inQ)
  w = pffloat4.getW(inQ)
  return pffloat4.setXYZ(1.0 - 2.0 * (y*y + z*z), 2.0 * (x*y + z*w), 2.0 * (z*x - y*w))

def axisY(inQ) :
  '''
  axisY(q) -> [x,y,z,0]
  '''
  #     2 ( x * y - z * w )
  # 1 - 2 ( x * x + z * z )
  #     2 ( y * z + x * w )
  x = pffloat4.getX(inQ)
  y = pffloat4.getY(inQ)
  z = pffloat4.getZ(inQ)
  w = pffloat4.getW(inQ)
  return pffloat4.setXYZ(2.0 * (x*y - z*w), 1.0 - 2.0 * (x*x + z*z), 2.0 * (y*z + x*w))

def axisZ(inQ) :
  '''
  axisZ(q) -> [x,y,z,0]
  '''
  #     2 ( x * z + y * w )
  #     2 ( y * z - x * w )
  # 1 - 2 ( x * x + y * y )
  x = pffloat4.getX(inQ)
  y = pffloat4.getY(inQ)
  z = pffloat4.getZ(inQ)
  w = pffloat4.getW(inQ)
  return pffloat4.setXYZ(2.0 * (x*z + y*w), 2.0 * (y*z - x*w), 1.0 - 2.0 * (x*x + y*y))

def normal(inQ) :
  '''
  normal(q) -> q
  '''
  scl = pffloat4.len4(inQ)
  if scl < 1.0e-10 : return pffloat4.axisW()
  return plusW(pffloat4.mulScalar(inQ, 1.0/scl))

def adjustW(inQ) :
  '''
  adjustW([x,y,z,_]) -> [x,y,z,w]
  '''
  sclXYZ = pffloat4.len3(inQ)
  if sclXYZ >= 1.0 : return pffloat4.setW0(pffloat4.mulScalar(inQ, 1.0/sclXYZ))
  w = pffloat1.sqrtClamp(1.0 - sclXYZ * sclXYZ)
  return pffloat4.setW(inQ, w)

def adjustXYZ(inQ) :
  '''
  adjustXYZ([_,_,_,w]) -> [x,y,z,w]
  '''
  w = pffloat4.getW(inQ)
  if w >= 1.0 : return pffloat4.axisW()
  sclXYZ = pffloat4.len3(inQ)
  lenXYZ = pffloat1.sqrtClamp(1.0 - w * w)
  if sclXYZ < 1.0e-10 : 
    x = pffloat4.getX(inQ)
    y = pffloat4.getY(inQ)
    z = pffloat4.getZ(inQ)
    absx = abs(x)
    absy = abs(y)
    absz = abs(z)
    if absx > absy : 
      if absx > absz : 
        if x >= 0.0 : return pffloat4.setXYZW(lenXYZ, 0.0, 0.0, w)
        else : return pffloat4.setXYZW(-lenXYZ, 0.0, 0.0, w)
      else :
        if z >= 0.0 : return pffloat4.setXYZW(0.0, 0.0, lenXYZ, w)
        else : return pffloat4.setXYZW(0.0, 0.0, -lenXYZ, w)
    else :
      if absy > absz : 
        if y >= 0.0 : return pffloat4.setXYZW(0.0, lenXYZ, 0.0, w)
        else : return pffloat4.setXYZW(0.0, -lenXYZ, 0.0, w)
      else :
        if z >= 0.0 : return pffloat4.setXYZW(0.0, 0.0, lenXYZ, w)
        else : return pffloat4.setXYZW(0.0, 0.0, -lenXYZ, w)
  return pffloat4.setW(pffloat4.mulScalar(inQ, lenXYZ/sclXYZ), w)

def inverse(inQ) :
  '''
  inverse(q) -> q^-1
  '''
  scl = pffloat4.len4(inQ)
  if scl < 1.0e-10 : return pffloat4.axisW()
  q = conjugate(inQ)
  return pffloat4.mulScalar(q, 1.0/(scl * scl))

def conjugate(inQ) :
  '''
  conjugate([x,y,z,w]) -> [-x,-y,-z,w]
  '''
  return pffloat4.copyW(pffloat4.neg(inQ), inQ)

def plusW(inQ) :
  '''
  plusW(q) -> q
  '''
  if pffloat4.getW(inQ) < 0.0 : return pffloat4.neg(inQ)
  else : return list(inQ)

def fromEuler(inOrd, inEul) :
  '''
  fromEuler(int, [degX,degY,degZ]) -> quaternion
  order : xyz=0,yzx=1,zxy=2,xzy=3,yxz=4,zyx=5
  '''
  sn = [0.0, 0.0, 0.0]
  cs = [0.0, 0.0, 0.0]
  for xyz in range(3) :
    deg = inEul[xyz] * 0.5
    sn[xyz] = pffloat1.sinDegree(deg)
    cs[xyz] = pffloat1.cosDegree(deg)
  qtx = 0.0
  qty = 0.0
  qtz = 0.0
  qtw = 1.0

  if inOrd == 1 or inOrd == 2 : # yzx zxy
    # zx : (sx,0,0,cx) * (0,0,sz,cz)
    x =  sn[0] * cs[2]
    y = -sn[0] * sn[2]
    z =  cs[0] * sn[2]
    w =  cs[0] * cs[2]
    if inOrd == 1 : 
      # yzx : (x,y,z,w) * (0,sy,0,cy)
      qtx = x * cs[1] - z * sn[1]
      qty = y * cs[1] + w * sn[1]
      qtz = z * cs[1] + x * sn[1]
      qtw = w * cs[1] - y * sn[1]
    else :
      # zxy : (0,sy,0,cy) * (x,y,z,w)
      qtx =  cs[1] * x + sn[1] * z
      qty =  sn[1] * w + cs[1] * y
      qtz = -sn[1] * x + cs[1] * z
      qtw =  cs[1] * w - sn[1] * y
    #}
  elif inOrd == 3 or inOrd == 4 : # xzy yxz
    # xz : (0,0,sz,cz) * (sx,0,0,cx)
    x = cs[2] * sn[0]
    y = sn[2] * sn[0]
    z = sn[2] * cs[0]
    w = cs[2] * cs[0]
    if inOrd == 3 :
      # xzy : (0,sy,0,cy) * (x,y,z,w)
      qtx =  cs[1] * x + sn[1] * z
      qty =  sn[1] * w + cs[1] * y
      qtz = -sn[1] * x + cs[1] * z
      qtw =  cs[1] * w - sn[1] * y
    else :
      # yxz : (x,y,z,w) * (0,sy,0,cy)
      qtx = x * cs[1] - z * sn[1]
      qty = y * cs[1] + w * sn[1]
      qtz = z * cs[1] + x * sn[1]
      qtw = w * cs[1] - y * sn[1]
    #}
  elif inOrd == 5 : # zyx
    # yx : (sx,0,0,cx) * (0,sy,0,cy)
    x = sn[0] * cs[1]
    y = cs[0] * sn[1]
    z = sn[0] * sn[1]
    w = cs[0] * cs[1]
    # (x,y,z,w) * (0,0,sz,cz)
    qtx = x * cs[2] + y * sn[2]
    qty = y * cs[2] - x * sn[2]
    qtz = z * cs[2] + w * sn[2]
    qtw = w * cs[2] - z * sn[2]
  else : # xyz
    # xy : (0,sy,0,cy) * (sx,0,0,cx)
    x =  cs[1] * sn[0]
    y =  sn[1] * cs[0]
    z = -sn[1] * sn[0]
    w =  cs[1] * cs[0]
    # xyz : (0,0,sz,cz) * (x,y,z,w)
    qtx = cs[2] * x - sn[2] * y
    qty = cs[2] * y + sn[2] * x
    qtz = cs[2] * z + sn[2] * w
    qtw = cs[2] * w - sn[2] * z
  return pffloat4.setXYZW(qtx, qty, qtz, qtw)

def  toEuler(inOrd, inQ) :
  '''
  toEuler(order, quaternion) -> euler
  order : xyz=0,yzx=1,zxy=2,xzy=3,yxz=4,zyx=5
  '''
  eul = pffloat4.zero()
  if inOrd == 1 :  # yzx
    scv = pffloat4.alignAxisYRotateX(axisY(inQ))
    eul = pffloat4.setX(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = fromAxisSinCos(pffloat4.axisX(), scv[0], scv[1])
    scv = pffloat4.alignAxisYRotateZ(scv[2])
    eul = pffloat4.setZ(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = multiply(qt, fromAxisSinCos(pffloat4.axisZ(), scv[0], scv[1]))

    v = pfvector.toLocalVectorByQuaternion(axisX(inQ), qt)
    dv = pfvector.alignAxisXRotateY(v)
    eul = pffloat4.setY(eul, dv[0])
  elif inOrd == 2 : # zxy
    scv = pffloat4.alignAxisZRotateY(axisZ(inQ))
    eul = pffloat4.setY(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = fromAxisSinCos(pffloat4.axisY(), scv[0], scv[1])
    scv = pffloat4.alignAxisZRotateX(scv[2])
    eul = pffloat4.setX(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = multiply(qt, fromAxisSinCos(pffloat4.axisX(), scv[0], scv[1]))

    v = pfvector.toLocalVectorByQuaternion(axisX(inQ), qt)
    dv = pfvector.alignAxisXRotateZ(v)
    eul = pffloat4.setZ(eul, dv[0])
  elif inOrd == 3 : # xzy
    scv = pffloat4.alignAxisXRotateY(axisX(inQ))
    eul = pffloat4.setY(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = fromAxisSinCos(pffloat4.axisY(), scv[0], scv[1])
    scv = pffloat4.alignAxisXRotateZ(scv[2])
    eul = pffloat4.setZ(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = multiply(qt, fromAxisSinCos(pffloat4.axisZ(), scv[0], scv[1]))

    v = pfvector.toLocalVectorByQuaternion(axisY(inQ), qt)
    dv = pfvector.alignAxisYRotateX(v)
    eul = pffloat4.setX(eul, dv[0])
  elif inOrd == 4 : # yxz
    scv = pffloat4.alignAxisYRotateZ(axisY(inQ))
    eul = pffloat4.setZ(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = fromAxisSinCos(pffloat4.axisZ(), scv[0], scv[1])
    scv = pffloat4.alignAxisYRotateX(scv[2])
    eul = pffloat4.setX(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = multiply(qt, fromAxisSinCos(pffloat4.axisX(), scv[0], scv[1]))

    v = pfvector.toLocalVectorByQuaternion(axisX(inQ), qt)
    dv = pfvector.alignAxisXRotateY(v)
    eul = pffloat4.setY(eul, dv[0])
  elif inOrd == 5 : # zyx
    scv = pffloat4.alignAxisZRotateX(axisZ(inQ))
    eul = pffloat4.setX(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = fromAxisSinCos(pffloat4.axisX(), scv[0], scv[1])
    scv = pffloat4.alignAxisZRotateY(scv[2])
    eul = pffloat4.setY(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = multiply(qt, fromAxisSinCos(pffloat4.axisY(), scv[0], scv[1]))

    v = pfvector.toLocalVectorByQuaternion(axisX(inQ), qt)
    dv = pfvector.alignAxisXRotateZ(v)
    eul = pffloat4.setZ(eul, dv[0])
  else : # xyz
    scv = pffloat4.alignAxisXRotateZ(axisX(inQ))
    eul = pffloat4.setZ(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = fromAxisSinCos(pffloat4.axisZ(), scv[0], scv[1])
    scv = pffloat4.alignAxisXRotateY(scv[2])
    eul = pffloat4.setY(eul, pffloat1.atan2Degree(scv[0], scv[1]))
    qt = multiply(qt, fromAxisSinCos(pffloat4.axisY(), scv[0], scv[1]))

    v = pfvector.toLocalVectorByQuaternion(axisY(inQ), qt)
    dv = pfvector.alignAxisYRotateX(v)
    eul = pffloat4.setX(eul, dv[0])

  return eul


def fromAxisDeg(inAx, inDeg) : 
  '''
  fromAxisDeg(ax,deg) -> [ax*sin(deg*0.5), cos(deg0.5)]
  '''
  ( sn, cs ) = pffloat1.sinCosDegree(inDeg * 0.5)
  return pffloat4.setW(pffloat4.mulScalar(inAx, sn), cs)

def fromAxisSinCos(inAx, inS, inC) : 
  '''
  setAxisSinCos(ax,sin(th),cos(th)) -> [sin(th*0.5)*ax, cos(th*0.5)]
  '''
  sssc = pffloat4.sinCosHalf(inC)
  qt = pffloat4.mul(pffloat4.setW1(inAx), sssc)
  if inS < 0.0 : return conjugate(qt)
  else : return qt

def toAxisDeg(inQ) :
  '''
  toAxisDeg(qt) -> ( [x,y,z,0], deg )
  '''
  deg = pffloat1.acosDegree(pffloat4.getW(inQ)) * 2.0
  ax = pffloat4.setW0(pffloat4.normal3(inQ))
  return ( ax, deg )

def log(inQ) : 
  '''
  log(qt) -> log qt
  qt == exp(log(qt))
  w > 0.0
  '''
  xyzSqr = pffloat4.dot3(inQ, inQ)
  if xyzSqr > 1.5e-15 : 
    rXYZ = pffloat1.rsqrtClamp(xyzSqr)
    at2 = pffloat1.atan2Radian(rXYZ * xyzSqr, pffloat4.getW(inQ)) * rXYZ
    return pffloat4.setW0(pffloat4.mulScalar(inQ, at2))
  else :
    return pffloat4.setW0(inQ)

def exp(inQ) : 
  '''
  exp(log(qt)) -> quaternion(exponential)
  '''
  xyzSqr = pffloat4.dot3(inQ, inQ)
  if xyzSqr > 2.601e-15 : 
    rXYZ = pffloat1.rsqrtClamp(xyzSqr)
    sncs = pffloat1.sinCosRadian(rXYZ * xyzSqr)
    if sncs[1] < 0.0 : return pffloat4.setW(pffloat4.mulScalar(inQ, -sncs[0] * rXYZ), sncs[1])
    else : return pffloat4.setW(pffloat4.mulScalar(inQ, sncs[0] * rXYZ), sncs[1])
  else :
    w = pffloat1.sqrtClamp(1.0 - xyzSqr)
    return pffloat4.setW(inQ, w)

def alignAxisXRotateZ(inV) :
  '''
  alignAxisXRotateZ(vec) -> ( quaternion, vec )
  '''
  scv = pffloat4.alignAxisXRotateZ(inV)
  return ( fromAxisSinCos(pffloat4.axisZ(), scv[0], scv[1]), scv[2] )

def alignAxisXRotateY(inV) :
  '''
  alignAxisXRotateY(vec) -> ( quaternion, vec )
  '''
  scv = pffloat4.alignAxisXRotateY(inV)
  return ( fromAxisSinCos(pffloat4.axisY(), scv[0], scv[1]), scv[2] )

def alignAxisYRotateZ(inV) : 
  '''
  alignAxisYRotateZ(vec) -> ( quaternion, vec )
  '''
  scv = pffloat4.alignAxisYRotateZ(inV)
  return ( fromAxisSinCos(pffloat4.axisZ(), scv[0], scv[1]), scv[2] )

def alignAxisYRotateX(inV) : 
  '''
  alignAxisYRotateX(vec) -> ( quaternion, vec )
  '''
  scv = pffloat4.alignAxisYRotateX(inV)
  return ( fromAxisSinCos(pffloat4.axisX(), scv[0], scv[1]), scv[2] )

def alignAxisZRotateY(inV) : 
  '''
  alignAxisZRotateY(vec) -> ( quaternion, vec )
  '''
  scv = pffloat4.alignAxisZRotateY(inV)
  return ( fromAxisSinCos(pffloat4.axisY(), scv[0], scv[1]), scv[2] )

def alignAxisZRotateX(inV) : 
  '''
  alignAxisZRotateX(vec) -> ( quaternion, vec )
  '''
  scv = pffloat4.alignAxisZRotateX(inV)
  return ( fromAxisSinCos(pffloat4.axisX(), scv[0], scv[1]), scv[2] )

def nearPlusMinus(inQA, inQB) :
  '''
  nearPlusMinus(qtA, qtB) -> 1 or -1
  '''
  p = pffloat4.sum(pffloat4.abs(pffloat4.add(inQA, inQB)))
  m = pffloat4.sum(pffloat4.abs(pffloat4.sub(inQA, inQB)))
  if (p > m) : return 1.0
  else : return -1.0

def fromVector(inFrom, inTo) : 
  '''
  fromVector(inFrom, inTo)
  '''
  ax = pffloat4.cross3(inFrom, inTo)
  dt = pffloat4.dot3(inFrom, inTo)
  qt = pffloat4.setW(ax, dt + 1.0)
  if pffloat4.getW(qt) <= 1.0e-10 : 
    absFrom = pffloat4.abs(inFrom)
    if pffloat4.getX(absFrom) > pffloat4.getY(absFrom) : ax = pffloat4.axisY()
    elif pffloat4.getZ(absFrom) > pffloat4.getX(absFrom) : ax = pffloat4.axisX()
    else : ax = pffloat4.axisZ()
    ax = pffloat4.cross3(inFrom, ax)
    vF = pffloat4.cross3(inFrom, ax)
    vT = pffloat4.cross3(inTo, ax)
    if dt < 0.0 : ax = pffloat4.sub(vF, vT)
    else : ax = pffloat4.add(vF, vT)
    qt = pffloat4.setW0(ax)
  return normal(qt)

def interpLinear(inQA, inQB, inRateB) : 
  '''
  interpLinear(qtA, qtB, rateB) -> (1-rateB) * qtA + rateB * qtB
  '''
  qt = pffloat4.interp(inQA, pffloat4.mulScalar(inQB, nearPlusMinus(inQA, inQB)), pffloat4.splat(inRateB))
  return normal(qt)

def slerp(inQA, inQB, inRateB) : 
  '''
  slerp(qtA, qtB, rateB) -> (1-rateB) * qtA + rateB * qtB
  '''
  qtB = pffloat4.mulScalar(inQB, nearPlusMinus(inQA, inQB))
  cs = pffloat4.dot4(inQA, qtB)
  sqrSn = max(1.0 - cs * cs, 0.0)
  if sqrSn > 1.0e-8 : 
    th = pffloat1.acosRadian(cs)
    rateA = pffloat1.sinRadian(th * (1.0 - inRateB))
    rateB = pffloat1.sinRadian(th * inRateB)
    qt = pffloat4.mulScalar(inQA, rateA)
    qt = pffloat4.madd(qtB, pffloat4.splat(rateB), qt)
    return normal(qt)
  else : 
    return interpLinear(inQA, qtB, inRateB)

def from2BoneIK(inAx, inUpper, inLower, inDist) : 
  '''
  from2BoneIK(ax,upper,lower,distance) -> ( qtUpper, qtLower, 0 or 1 or -1 )
  '''
  if inDist >= (inUpper + inLower) : 
    return ( pffloat4.axisW(), pffloat4.axisW(), 1 )
  elif inDist <= abs(inUpper - inLower) : 
    if inUpper > inLower : qtUp = pffloat4.axisW()
    else : qtUp = pffloat4.setW0(inAx)
    return ( qtUp, pffloat4.setW0(pffloat4.neg(inAx)), -1 )
  else :
    sqrUpper = inUpper * inUpper
    sqrLower = inLower * inLower
    sqrDist = inDist * inDist

    upperCs = ( sqrDist + sqrUpper - sqrLower ) / ( 2.0 * inDist * inUpper )
    qtUp = fromAxisSinCos(inAx, 0.1, upperCs)
    lowerCs = ( sqrDist - sqrUpper - sqrLower ) / ( 2.0 * inUpper * inLower )
    qtLow = fromAxisSinCos(pffloat4.neg(inAx), 0.1, lowerCs)
    return ( qtUp, qtLow, 0 )

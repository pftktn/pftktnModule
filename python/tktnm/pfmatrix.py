# -*- coding: utf-8 -*-
'''
matrixの操作を行う関数群

See Copyright(LICENSE.txt) for the status of this software.
 
Author: Takeharu TANIMURA <tanie@kk.iij4u.or.jp>
'''

import math

from . import pffloat1
from . import pffloat4
from . import pfquaternion
from . import pfvector


def getRow(inV, inRowIndex) :
  '''
  getRow([r0,r1,r2,r3], 1) : r1
  '''
  return list(inV[inRowIndex*4:inRowIndex*4+4])
def setRow(inV, inRow, inRowIndex) :
  '''
  setRow([r0,r1,r2,r3], rX, 1) : [r0,rX,r2,r3]
  '''
  ofs = inRowIndex*4
  retVal = list(inV)
  for idx in range(4) :
    retVal[ofs+idx] = inRow[idx]
  return retVal

def getColumn(inV, inColumnIndex) :
  '''
  getColumn([r0,r1,r2,r3], col) : [r0[col], r1[col], r2[col], r3[col]]
  '''
  retVal = [0.0] * 4
  for idx in range(4) :
    retVal[idx] = inV[idx*4+inColumnIndex]
  return retVal
def setColumn(inV, inColumn, inColumnIndex) :
  '''
  setColumn([r0,r1,r2,r3], col, idx) : r0[idx]=col[0], r1[idx]=col[1] ...
  '''
  retVal = list(inV)
  for idx in range(4) :
    retVal[idx*4+inColumnIndex] = inColumn[idx]
  return retVal

def identity() : 
  '''
  identity() : [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
  '''
  return list([1.0,0.0,0.0,0.0, 0.0,1.0,0.0,0.0, 0.0,0.0,1.0,0.0, 0.0,0.0,0.0,1.0])

def zero() :
  '''
  zero() : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
  '''
  return [0.0] * 16

def multiply(inParent, inChild) :
  '''
  multiply(m0, m1) : m0 * m1
  '''
  mtx = zero()
  for chRowIdx in range(4) :
    chRow = getRow(inChild, chRowIdx)
    for prntColIdx in range(4) :
      prntCol = getColumn(inParent, prntColIdx)
      mtx[chRowIdx*4 + prntColIdx] = pffloat4.dot4(chRow, prntCol)
  return mtx

def add(inMtxA, inMtxB) :
  '''
  add([a,...], [b,...]) : [a+b,...]
  '''
  mtx = zero()
  for idx in range(16) :
    mtx[idx] = inMtxA[idx] + inMtxB[idx]
  return mtx

def sub(inMtxA, inMtxB) :
  '''
  sub([a,...], [b,...]) : [a-b,...]
  '''
  mtx = zero()
  for idx in range(16) :
    mtx[idx] = inMtxA[idx] - inMtxB[idx]
  return mtx

def sum(inMtx) :
  '''
  sum([a,b,...]) : a+b+...
  '''
  v = inMtx[15]
  for idx in range(15) : v = v + inMtx[idx]
  return v

def abs(inMtx) :
  '''
  abs([a,...]) : [fabs(a),...]
  '''
  mtx = zero()
  for idx in range(16) : mtx[idx] = math.fabs(inMtx[idx])
  return mtx

def transpose(inMtx) :
  '''
  transpose(mtx) : transposed mtx
  '''
  mtx = zero()
  for rowIdx in range(4) :
    for colIdx in range(4) :
      mtx[colIdx*4+rowIdx] = inMtx[rowIdx*4+colIdx]
  return mtx

def compose(translate=None, quaternion=None, shear=None, scale=None) :
  '''
  compose(translate, quaternion, shear, scale) : compose transformation matrix
  '''
  mtx = identity()
  if translate is not None : 
    mtx = fromTranslate(translate)
  if quaternion is not None :
    mtx = multiply(mtx, fromQuaternion(quaternion))
  if shear is not None or scale is not None :
    shr = [ 0.0, 0.0, 0.0 ]
    scl = [ 1.0, 1.0, 1.0 ]
    if shear is not None : shr = shear
    if scale is not None : scl = scale
    mtx = multiply(mtx, fromShearScale(shr, scl))
  return mtx

def decompose(inV) :
  '''
  decompose(mtx) : ( translate, quaternion, shear, scale )
  '''
  ( shr, scl ) = toShearScale(inV)
  mtxQtTrn = multiply(inV, inverseFromShearScale(shr, scl))
  qt = toQuaternion(mtxQtTrn)
  trn = toTranslate(mtxQtTrn)
  return ( trn, qt, shr, scl )

def inverseTransform(inV) :
  '''
  inverseTransform(mtx) : mtx^-1
  '''
  ( shr, scl ) = toShearScale(inV)
  mtxInvShrScl = inverseFromShearScale(shr, scl)
  mtxRotTrn = multiply(inV, mtxInvShrScl)
  trn = toTranslate(mtxRotTrn)
  mtxRot = setRow(mtxRotTrn, pffloat4.axisW(), 3)
  mtxInvRot = transpose(mtxRot)
  mtx = multiply(mtxInvShrScl, mtxInvRot)
  mtx = multiply(mtx, fromTranslate(pffloat4.neg(trn)))
  return mtx

def fromScale(inScale) :
  '''
  fromScale(s) : scale matrix
  '''
  mtx = zero()
  mtx[0] = inScale[0]
  mtx[5] = inScale[1]
  mtx[10] = inScale[2]
  mtx[15] = 1.0
  return mtx

def fromShear(inShear) :
  '''
  fromShear(s) : shear matrix
  '''
  mtx = zero()
  mtx[0] = mtx[5] = mtx[10] = mtx[15] = 1.0
  mtx[4] = inShear[0]
  mtx[8] = inShear[1]
  mtx[9] = inShear[2]
  return mtx

def fromShearScale(inShear, inScale) :
  '''
  fromShearScale(shr, scl) : shear, scale matrix
  '''
  # |1  0  0| |Sx  0  0|
  # |Hx 1  0| | 0 Sy  0|
  # |Hy Hz 1| | 0  0 Sz|
  # |Sx    0    0|
  # |HxSy Sy    0|
  # |HySz HzSz Sz|
  mtx = zero()
  mtx[15] = 1.0

  mtx[0] = inScale[0]

  mtx[4] = inShear[0] * inScale[1]
  mtx[5] = inScale[1]

  mtx[8] = inShear[1] * inScale[2]
  mtx[9] = inShear[2] * inScale[2]
  mtx[10] = inScale[2]

  return mtx

def fromQuaternion(inQ) :
  '''
  fromQuaternion(q) : quaternion matrix
  '''
  mtx = zero()
  mtx[15] = 1.0

  ax = pfquaternion.axisX(inQ)
  mtx[0] = ax[0]
  mtx[1] = ax[1]
  mtx[2] = ax[2]
  ax = pfquaternion.axisY(inQ)
  mtx[4] = ax[0]
  mtx[5] = ax[1]
  mtx[6] = ax[2]
  ax = pfquaternion.axisZ(inQ)
  mtx[8] = ax[0]
  mtx[9] = ax[1]
  mtx[10] = ax[2]

  return mtx

def fromTranslate(inV) :
  '''
  fromTranslate(q) : translate matrix
  '''
  mtx = zero()
  mtx[12] = inV[0]
  mtx[13] = inV[1]
  mtx[14] = inV[2]
  mtx[0] = mtx[5] = mtx[10] = mtx[15] = 1.0
  return mtx

def inverseFromQuaternion(inQ) :
  '''
  fromQuaternion(q) : quaternion matrix^-1
  '''
  mtx = zero()
  mtx[15] = 1.0

  ax = pfquaternion.axisX(inQ)
  mtx[0] = ax[0]
  mtx[4] = ax[1]
  mtx[8] = ax[2]
  ax = pfquaternion.axisY(inQ)
  mtx[1] = ax[0]
  mtx[5] = ax[1]
  mtx[9] = ax[2]
  ax = pfquaternion.axisZ(inQ)
  mtx[2] = ax[0]
  mtx[6] = ax[1]
  mtx[10] = ax[2]

  return mtx

def inverseFromTranslate(inV) :
  '''
  inverseFromTranslate(q) : translate matrix^-1
  '''
  return fromTranslate(pffloat4.neg(inV))

def inverseFromScale(inScl) :
  '''
  inverseFromScale(s) : scale matrix^-1
  '''
  mtx = zero()
  invScl = pffloat4.div3(pffloat4.axisXYZ(), inScl)

  mtx[0] = invScl[0]
  mtx[5] = invScl[1]
  mtx[10] = inScl[2]
  mtx[15] = 1.0
  return mtx

def inverseFromShear(inShr) :
  '''
  inverseFromShear(s) : shear matrix
  '''
  invShr = pffloat4.neg(inShr)
  invShrY = pffloat4.getX(invShr) * pffloat4.getZ(invShr) + pffloat4.getY(invShr)
  invShr = pffloat4.setY(invShr, invShrY)
  
  mtx = zero()
  mtx[0] = mtx[5] = mtx[10] = mtx[15] = 1.0
  mtx[4] = invShr[0]
  mtx[8] = invShr[1]
  mtx[9] = invShr[2]
  return mtx

def inverseFromShearScale(inShr, inScl) :
  '''
  inverseFromShearScale(shr, scl) : shear,scale matrix^-1
  '''
  # |Sx  0  0| |1  0  0|
  # | 0 Sy  0| |Hx 1  0|
  # | 0  0 Sz| |Hy Hz 1|
  # |Sx    0    0|
  # |HxSx Sy    0|
  # |HySx HzSy Sz|
  invScl = pffloat4.div3(pffloat4.axisXYZ(), inScl)
  invShr = pffloat4.neg(inShr)
  invShrY = pffloat4.getX(invShr) * pffloat4.getZ(invShr) + pffloat4.getY(invShr)
  invShr = pffloat4.setY(invShr, invShrY)
  
  mtx = zero()
  mtx[15] = 1.0

  mtx[0] = invScl[0]

  mtx[4] = invShr[0] * invScl[0]
  mtx[5] = invScl[1]

  mtx[8] = invShr[1] * invScl[0]
  mtx[9] = invShr[2] * invScl[1]
  mtx[10] = invScl[2]

  return mtx

def toShearScale(inMtx) :
  '''
  toShearScale(mtx) : ( shear, scale )
  '''
  # |Xa Xb Xc| |1  0  0| |Sx  0  0|
  # |Ya Yb Yc| |Hx 1  0| | 0 Sy  0|
  # |Za Zb Zc| |Hy Hz 1| | 0  0 Sz|
  #
  # |Xa           Xb           Xc          | |Sx  0  0|
  # |XaHx+Ya      XbHx+Yb      XcHx+Yc     | | 0 Sy  0|
  # |XaHy+YaHz+Za XbHy+YbHz+Zb XcHy+YcHz+Zc| | 0  0 Sz|
  #
  # |XaSx               XbSx               XcSx              |
  # |XaHxSy+YaSy        XbHxSy+YbSy        XcHxSy+YcSy       |
  # |XaHySz+YaHzSz+ZaSz XbHySz+YbHzSz+ZbSz XcHySz+YcHzSz+ZcSz|

  # XaYa + XbYb + XcYc = 0
  # YaZa + YbZb + YcZc = 0
  # XaZa + XbZb + XcZc = 0
  #
  # XaXa + XbXb + XcXc = 1
  # YaYa + YbYb + YcYc = 1
  # ZaZa + ZbZb + ZcZc = 1
  vX = getRow(inMtx, 0)
  vY = getRow(inMtx, 1)
  vZ = getRow(inMtx, 2)
  sqrX = pffloat4.dot3(vX, vX)
  sclX = pffloat1.sqrtClamp(sqrX)
  vTmp = pffloat4.cross3(vX, vY)
  if pffloat4.dot3(vTmp, vZ) < 0.0 : sclX = -sclX

  # dot(vX,vY)
  # XaSx(XaHxSy+YaSy) + XbSx(XbHxSy+YbSy) + XcSx(XcHxSy+YcSy) = D
  # XaXaHxSxSy + XbXbHxSxSy + XcXcHxSxSy + SxSy(XaYa + XbYb + XcYc) = D
  # XaXaHxSxSy + XbXbHxSxSy + XcXcHxSxSy = D
  # (XaXa + XbXb + XcXc)HxSxSy = D
  # HxSxSy = D

  # length(vY)
  # (XaHxSy+YaSy)(XaHxSy+YaSy) + (XbHxSy+YbSy)(XbHxSy+YbSy) + (XcHxSy+YcSy)(XcHxSy+YcSy) = H
  #   XaXaHxHxSySy + 2XaYaHxSySy + YaYaSySy
  # + XbXbHxHxSySy + 2XbYbHxSySy + YbYbSySy
  # + XcXcHxHxSySy + 2XcYcHxSySy + YcYcSySy = H
  #  
  # HxHxSySy(XaXa + XbXb + XcXc) + 2HxSySy(XaYa + XbYb + XcYc) + SySy(YaYa + YbYb + YcYc) = H
  # HxHxSySy + SySy = H
  # HxHxSySy = H - SySy
  # HxHx = (H - SySy)/(SySy)

  # HxHxSxSxSySy = DD
  # SxSxSySy(H - SySy)/(SySy) = DD
  # SxSx(H - SySy) = DD
  # SxSxH - SxSxSySy = DD
  # SxSxSySy = SxSxH - DD
  # SySy = (SxSxH - DD)/(SxSx)
  # 
  # HxHxSxSxH/(HxHx + 1) = DD
  # HxHxSxSxH = DD(HxHx + 1)
  # HxHx(SxSxH - DD) = DD
  # HxHx = DD/(SxSxH - DD)
  sqrY = pffloat4.dot3(vY, vY)  # H
  dtXY = pffloat4.dot3(vX, vY)  # D
  sclY = pffloat1.sqrtClamp(sqrY - (dtXY*dtXY/sqrX))

  # Hx = D/(SxSy)
  shrXY = dtXY / (sclX*sclY)

  # sqrLength(vZ)
  # HyHySzSz + HzHzSzSz + SzSz = I
  #*
  # dot(vX,vZ)
  # HySxSz = E
  # HySz = E/Sx
  #
  # dot(vY,vZ)
  # HzSz = (F - HxHySySz)/Sy
  # HzSz = (SxF - HxHySxSySz)/(SxSy)
  # HzSz = (SxF - HxSyE)/(SxSy)
  #
  # EE/SxSx + HzHzSzSz + SzSz = I
  # EE/SxSx + (SxF - HxSyE)(SxF - HxSyE)/(SxSxSySy) + SzSz = I
  # SzSz = I - EE/SxSx - (SxF - HxSyE)(SxF - HxSyE)/(SxSxSySy)
  sqrZ = pffloat4.dot3(vZ, vZ)  # I
  dtXZ = pffloat4.dot3(vX, vZ)  # E
  dtYZ = pffloat4.dot3(vY, vZ)  # F
  shrYZ = (sclX*dtYZ - shrXY*sclY*dtXZ) / (sclX*sclY)
  sclZ = pffloat1.sqrtClamp(sqrZ - (dtXZ*dtXZ)/sqrX - shrYZ*shrYZ)

  # dot(vX,vZ)
  # Hy = E/(SxSz)
  shrXZ = dtXZ/(sclX*sclZ)

  # dot(vY,vZ)
  # Hz = (SxF - HxSyE)/(SxSySz)
  shrYZ = shrYZ/sclZ

  return ( pffloat4.setXYZ(shrXY, shrXZ, shrYZ), pffloat4.setXYZ(sclX, sclY, sclZ) )

def toTranslate(inMtx) :
  '''
  toTranslate(mtx) : translate
  '''
  v = getRow(inMtx, 3)
  return pffloat4.setW0(v)

def toQuaternion(inM) :
  '''
  toQuaternion(mtx) : quaternion
  '''
  vX = getRow(inM, 0)
  vY = getRow(inM, 1)
  vZ = getRow(inM, 2)
  dpX = math.fabs(vX[0])
  dpY = math.fabs(vY[1])
  dpZ = math.fabs(vZ[2])
  if dpX < dpY and dpX < dpZ :
    qt = pfquaternion.fromVector(pffloat4.axisX(), vX)
    vTmp = pfvector.toLocalVectorByQuaternion(vY, qt)
    qtv = pfquaternion.alignAxisYRotateX(vTmp)
    return pfquaternion.multiply(qt, qtv[0])
  elif dpY < dpZ :
    qt = pfquaternion.fromVector(pffloat4.axisY(), vY)
    vTmp = pfvector.toLocalVectorByQuaternion(vX, qt)
    qtv = pfquaternion.alignAxisXRotateY(vTmp)
    return pfquaternion.multiply(qt, qtv[0])
  else :
    qt = pfquaternion.fromVector(pffloat4.axisZ(), vZ)
    vTmp = pfvector.toLocalVectorByQuaternion(vX, qt)
    qtv = pfquaternion.alignAxisXRotateZ(vTmp)
    return pfquaternion.multiply(qt, qtv[0])

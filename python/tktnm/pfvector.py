'''
vectorの操作を行う関数群

See Copyright(LICENSE.txt) for the status of this software.
 
Author: Takeharu TANIMURA <tanie@kk.iij4u.or.jp>
'''

import math

from . import pffloat1
from . import pffloat4
from . import pfquaternion
from . import pfmatrix



def toWorldVectorByMatrix(inV, inM) :
  '''
  toWorldVectorByMatrix(vec,mtx) -> vec
  '''
  vX = pfmatrix.getRow(inM, 0)
  vY = pfmatrix.getRow(inM, 1)
  vZ = pfmatrix.getRow(inM, 2)
  vX = pffloat4.mulScalar(vX, pffloat4.getX(inV))
  vY = pffloat4.mulScalar(vY, pffloat4.getY(inV))
  vZ = pffloat4.mulScalar(vZ, pffloat4.getZ(inV))
  v = pffloat4.add(vX, vY)
  v = pffloat4.add(v, vZ)
  return v

def toWorldPositionByMatrix(inV, inM) :
  '''
  toWorldPositionByMatrix(pos,mtx) -> pos
  '''
  v = toWorldVectorByMatrix(inV, inM)
  pos = pfmatrix.getRow(inM, 3)
  pos = pffloat4.add(pos, v)
  return pos

def toLocalVectorByMatrix(inV, inM) :
  '''
  toLocalVectorByMatrix(vec,mtx) -> vec
  '''
  invM = pfmatrix.inverseTransform(inM)
  return toWorldVectorByMatrix(inV, invM)

def toLocalPositionByMatrix(inV, inM) :
  '''
  toLocalPositionByMatrix(pos,mtx) -> pos
  '''
  invM = pfmatrix.inverseTransform(inM)
  return toWorldPositionByMatrix(inV, invM)

def toWorldVectorByQuaternion(inV, inQ) : 
  '''
  toWorldVectorByQuaternion(vec,qt) -> vec
  '''
  return pfquaternion.sandwich(inQ, pffloat4.setW0(inV))

def toLocalVectorByQuaternion(inV, inQ) : 
  '''
  toLocalVectorByQuaternion(vec,qt) -> vec
  '''
  return pfquaternion.sandwichInverse(inQ, pffloat4.setW0(inV))

def alignAxisXRotateZ(inV) : 
  '''
  alignAxisXRotateZ(vec) -> ( rotateZ(degree), vec )
  '''
  scv = pffloat4.alignAxisXRotateZ(inV)
  return ( pffloat1.atan2Degree(scv[0], scv[1]), scv[2] )

def alignAxisXRotateY(inV) : 
  '''
  alignAxisXRotateY(vec) -> ( rotateY(degree), vec )
  '''
  scv = pffloat4.alignAxisXRotateY(inV)
  return ( pffloat1.atan2Degree(scv[0], scv[1]), scv[2] )

def alignAxisYRotateZ(inV) : 
  '''
  alignAxisYRotateZ(vec) -> ( rotateZ(degree), vec )
  '''
  scv = pffloat4.alignAxisYRotateZ(inV)
  return ( pffloat1.atan2Degree(scv[0], scv[1]), scv[2] )

def alignAxisYRotateX(inV) : 
  '''
  alignAxisYRotateX(vec) -> ( rotateX(degree), vec )
  '''
  scv = pffloat4.alignAxisYRotateX(inV)
  return ( pffloat1.atan2Degree(scv[0], scv[1]), scv[2] )

def alignAxisZRotateY(inV) : #
  '''
  alignAxisZRotateY(vec) -> ( rotateY(degree), vec )
  '''
  scv = pffloat4.alignAxisZRotateY(inV)
  return ( pffloat1.atan2Degree(scv[0], scv[1]), scv[2] )

def alignAxisZRotateX(inV) : 
  '''
  alignAxisZRotateX(vec) -> ( rotateX(degree), vec )
  '''
  scv = pffloat4.alignAxisZRotateX(inV)
  return ( pffloat1.atan2Degree(scv[0], scv[1]), scv[2] )

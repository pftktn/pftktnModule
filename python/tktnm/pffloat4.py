# -*- coding: utf-8 -*-
'''
float4成分の操作を行う関数群

See Copyright(LICENSE.txt) for the status of this software.
 
Author: Takeharu TANIMURA <tanie@kk.iij4u.or.jp>
'''

import math
import random

from . import pffloat1

def zero() : 
  '''
  zero() -> [0,0,0,0]
  '''
  return [ 0.0, 0.0, 0.0, 0.0 ]

def one() : 
  '''
  one() -> [1,1,1,1]
  '''
  return [ 1.0, 1.0, 1.0, 1.0 ]

def axisX() : 
  '''
  axisX() -> [1,0,0,0]
  '''
  return [ 1.0, 0.0, 0.0, 0.0 ]

def axisXW() : 
  '''
  axisXW() -> [1,0,0,1]
  '''
  return [ 1.0, 0.0, 0.0, 1.0 ]

def axisY() : 
  '''
  axisY() -> [0,1,0,0]
  '''
  return [ 0.0, 1.0, 0.0, 0.0 ]

def axisYW() : 
  '''
  axisYW() -> [0,1,0,1]
  '''
  return [ 0.0, 1.0, 0.0, 1.0 ]

def axisZ() : 
  '''
  axisZ() -> [0,0,1,0]
  '''
  return [ 0.0, 0.0, 1.0, 0.0 ]

def axisZW() : 
  '''
  axisZW() -> [0,0,1,1]
  '''
  return [ 0.0, 0.0, 1.0, 1.0 ]

def axisW() : 
  '''
  axisW() -> [0,0,0,1]
  '''
  return [ 0.0, 0.0, 0.0, 1.0 ]

def axisXYZ() :
  '''
  axisXYZ() -> [1,1,1,0]
  '''
  return [ 1.0, 1.0, 1.0, 0.0 ]

def splat(inV) : 
  '''
  splat(v) -> [v,v,v,v]
  '''
  return [ float(inV), float(inV), float(inV), float(inV) ]

def replicateX(inXYZW) : 
  '''
  replicateX([x,y,z,w]) -> [x,x,x,x]
  '''
  return splat(getX(inXYZW))

def replicateY(inXYZW) : 
  '''
  replicateY([x,y,z,w]) -> [y,y,y,y]
  '''
  return splat(getY(inXYZW))

def replicateZ(inXYZW) : 
  '''
  replicateZ([x,y,z,w]) -> [z,z,z,z]
  '''
  return splat(getZ(inXYZW))

def replicateW(inXYZW) : 
  '''
  replicateW([x,y,z,w]) -> [w,w,w,w]
  '''
  return splat(getW(inXYZW))

def getX(inXYZW) : 
  '''
  getX([x,y,z,w]) -> x
  '''
  return inXYZW[0]

def setX(inXYZW, inV) : 
  '''
  setX([x,y,z,w],v) -> [v,y,z,w]
  '''
  tmp = list(inXYZW)
  tmp[0] = inV
  return tmp

def getY(inXYZW) : 
  '''
  getY([x,y,z,w]) -> y
  '''
  return inXYZW[1]

def setY(inXYZW, inV) : 
  '''
  setY([x,y,z,w],v) -> [x,v,z,w]
  '''
  tmp = list(inXYZW)
  tmp[1] = inV
  return tmp

def getZ(inXYZW) : 
  '''
  getZ([x,y,z,w]) -> z
  '''
  return inXYZW[2]

def setZ(inXYZW, inV) : 
  '''
  setZ([x,y,z,w],v) -> [x,y,v,w]
  '''
  tmp = list(inXYZW)
  tmp[2] = inV
  return tmp

def getW(inXYZW) : 
  '''
  getW([x,y,z,w]) -> w
  '''
  if len(inXYZW) < 4 : return 0.0
  else : return inXYZW[3]

def setW(inXYZW, inV) : 
  '''
  setW([x,y,z,w],v) -> [x,y,z,v]
  '''
  return [inXYZW[0], inXYZW[1], inXYZW[2], inV]

def setW0(inXYZW) : 
  '''
  setW0([x,y,z,w]) -> [x,y,z,0]
  '''
  return [inXYZW[0], inXYZW[1], inXYZW[2], 0.0]

def setW1(inXYZW) : 
  '''
  setW1([x,y,z,w]) -> [x,y,z,1]
  '''
  return [inXYZW[0], inXYZW[1], inXYZW[2], 1.0]

def setXYZW(inX, inY, inZ, inW) : 
  '''
  setXYZW(x,y,z,w) -> [x,y,z,w]
  '''
  return [ inX, inY, inZ, inW ]

def set3(inXYZ) :
  '''
  set3(xyz) -> [xyz[0],xyz[1],xyz[2],0]
  '''
  return [ inXYZ[0], inXYZ[1], inXYZ[2], 0.0 ]

def setXYZ(inX, inY, inZ) : 
  '''
  setXYZ(x,y,z) -> [x,y,z,0]
  '''
  return [ inX, inY, inZ, 0.0 ]

def getXYZW(inV) : return [getX(inV), getY(inV), getZ(inV), getW(inV)]
def getXYZ(inV) : 
  '''
  getXYZ([x,y,z,_]) : [x,y,z]
  '''
  return [getX(inV), getY(inV), getZ(inV)]

def copyW(inXYZ, inW) : 
  '''
  copyW([x,y,z,_],[_,_,_,w]) -> [x,y,z,w]
  '''
  return [ inXYZ[0], inXYZ[1], inXYZ[2], inW[3] ]

def randomRange(inMin, inMax) : 
  '''
  randomRange(min,max) -> [ random(min,max), ...]
  '''
  return [ random.uniform(inMin, inMax), random.uniform(inMin, inMax), random.uniform(inMin, inMax), random.uniform(inMin, inMax) ]

def __applyScalar(inFunc, inCnt, inA, inB) : 
  tmp = getXYZW(inA)
  for idx in range(inCnt) : tmp[idx] = inFunc(tmp[idx], inB)
  return tmp

def addScalar(inXYZW, inV) : 
  '''
  addScalar([x,y,z,w],v) -> [x+v,y+v,z+v,w+v]
  '''
  return __applyScalar(lambda a,b : a+b, 4, inXYZW, inV)

def subScalar(inXYZW, inV) : 
  '''
  subScalar([x,y,z,w],v) -> [x-v,y-v,z-v,w-v]
  '''
  return __applyScalar(lambda a,b : a-b, 4, inXYZW, inV)

def mulScalar(inXYZW, inV) : 
  '''
  mulScalar([x,y,z,w],v) -> [x*v,y*v,z*v,w*v]
  '''
  return __applyScalar(lambda a,b : a*b, 4, inXYZW, inV)

def neg(inXYZW) : 
  '''
  neg([x,y,z,w]) -> [-x,-y,-z,-w]
  '''
  return mulScalar(inXYZW, -1.0)

def __applyABList(inFunc, inCnt, inA, inB) : 
  tmpA = getXYZW(inA)
  tmpB = getXYZW(inB)
  for idx in range(inCnt) : tmpA[idx] = inFunc(tmpA[idx], tmpB[idx])
  return tmpA

def add(inA, inB) : 
  '''
  add([x,y,z,w],[a,b,c,d]) -> [x+a,y+b,z+c,w+d]
  '''
  return __applyABList(lambda a,b : a+b, 4, inA, inB)

def sub(inA, inB) : 
  '''
  sub([x,y,z,w],[a,b,c,d]) -> [x-a,y-b,z-c,w-d]
  '''
  return __applyABList(lambda a,b : a-b, 4, inA, inB)

def mul(inA, inB) : 
  '''
  mul([x,y,z,w],[a,b,c,d]) -> [x*a,y*b,z*c,w*d]
  '''
  return __applyABList(lambda a,b : a*b, 4, inA, inB)

def div(inA, inB) :
  '''
  div([x,y,z,w],[a,b,c,d]) -> [x/a,y/b,z/c,w/d]
  '''
  return __applyABList(lambda a,b : a/b, 4, inA, inB)

def div3(inA, inB) :
  '''
  div3([x,y,z,w],[a,b,c,_]) -> [x/a,y/b,z/c,w]
  '''
  xyz = __applyABList(lambda a,b : a/b, 3, inA, inB)
  return copyW(xyz, inA)

def isLT(inA, inB) : 
  '''
  isLT([x,y,z,w],[a,b,c,d]) -> [x<a,y<b,z<c,w<d]
  '''
  return __applyABList(lambda a,b : a<b, 4, inA, inB)

def isGT(inA, inB) : 
  '''
  isGT([x,y,z,w],[a,b,c,d]) -> [x>a,y>b,z>c,w>d]
  '''
  return __applyABList(lambda a,b : a>b, 4, inA, inB)

def isLTEq(inA, inB) : 
  '''
  isLTEq([x,y,z,w],[a,b,c,d]) -> [x<=a,y<=b,z<=c,w<=d]
  '''
  return __applyABList(lambda a,b : a<=b, 4, inA, inB)

def isGTEq(inA, inB) : 
  '''
  isGTEq([x,y,z,w],[a,b,c,d]) -> [x>=a,y>=b,z>=c,w>=d]
  '''
  return __applyABList(lambda a,b : a>=b, 4, inA, inB)

def __applyABCList(inFunc, inCnt, inA, inB, inC) : 
  tmpA = getXYZW(inA)
  tmpB = getXYZW(inB)
  tmpC = getXYZW(inC)
  for idx in range(inCnt) : tmpA[idx] = inFunc(tmpA[idx], tmpB[idx], tmpC[idx])
  return tmpA

def madd(inA, inB, inC) : 
  '''
  madd([a,,,],[b,,,],[c,,,]) -> [a*b+c,,,]
  '''
  return __applyABCList(lambda a,b,c : a*b+c, 4, inA, inB, inC)

def nmsub(inA, inB, inC) : 
  '''
  nmsub([a,,,],[b,,,],[c,,,]) -> [c-a*b,,,]
  '''
  return __applyABCList(lambda a,b,c : c-a*b, 4, inA, inB, inC)

def msub(inA, inB, inC) : 
  '''
  msub([a,,,],[b,,,],[c,,,]) -> [a*b-c,,,]
  '''
  return __applyABCList(lambda a,b,c : a*b-c, 4, inA, inB, inC)

def nmadd(inA, inB, inC) : 
  '''
  nmadd([a,,,],[b,,,],[c,,,]) -> [-a*b-c,,,]
  '''
  return __applyABCList(lambda a,b,c : -a*b-c, 4, inA, inB, inC)

def hadd(inA, inB) : 
  '''
  hadd([a,b,c,d],[x,y,z,w]) -> [a+b,x+y,c+d,z+w]
  '''
  return [ getX(inA) + getY(inA), getX(inB) + getY(inB), getZ(inA) + getW(inA), getZ(inB) + getW(inB) ]

def hsub(inA, inB) : 
  '''
  hsub([a,b,c,d],[x,y,z,w]) -> [a-b,x-y,c-d,z-w]
  '''
  return [ getX(inA) - getY(inA), getX(inB) - getY(inB), getZ(inA) - getW(inA), getZ(inB) - getW(inB) ]

def addsub(inA, inB) :
  '''
  addsub([a,b,c,d],[x,y,z,w]) -> [a-x,b+y,c-z,d+w]
  '''
  return [ getX(inA) - getX(inB), getY(inA) + getY(inB), getZ(inA) - getZ(inB), getW(inA) + getW(inB) ]

def maddsub(inA, inB, inC) : 
  '''
  maddsub([a,b,c,d],[x,y,z,w],[o,p,q,r]) -> [a*x-o,b*y+p,c*z-q,c*w+w]
  '''
  return addsub(mul(inA, inB), inC)

def msubadd(inA, inB, inC) : 
  '''
  msubadd([a,b,c,d],[x,y,z,w],[o,p,q,r]) -> [a*x+o,b*y-p,c*z+q,c*w-w]
  '''
  return addsub(mul(inA, inB), neg(inC))

def __applyFunction(inFunc, inCnt, inA) : 
  tmpA = getXYZW(inA)
  for idx in range(inCnt) : tmpA[idx] = inFunc(tmpA[idx])
  return tmpA

def isNanInf(inXYZW) : 
  '''
  isNanInf([x,y,z,w]) -> [isNanInf(x), isNanInf(y), isNanInf(z), isNanInf(w)]
  '''
  return __applyFunction(lambda a : pffloat1.isNanInf(a), 4, inXYZW)

def abs(inXYZW) : 
  '''
  abs([x,y,z,w]) -> [math.fabs(x),math.fabs(y),math.fabs(z),math.fabs(w)]
  '''
  return __applyFunction(lambda a : math.fabs(a), 4, inXYZW)

def sum(inXYZW) : 
  '''
  sum([x,y,z,w]) -> x+y+z+w
  '''
  return inXYZW[0] + inXYZW[1] + inXYZW[2] + inXYZW[3]

def sum3(inXYZW) : 
  '''
  sum([x,y,z,_]) -> x+y+z
  '''
  return inXYZW[0] + inXYZW[1] + inXYZW[2]

def dot4(inA, inB) : 
  '''
  dot4([x,y,z,w],[a,b,c,d]) -> x*a+y*b+z*c+w*d
  '''
  m4 = mul(inA, inB)
  return sum(m4)

def dot3(inA, inB) : 
  '''
  dot3([x,y,z,w],[a,b,c,d]) -> x*a+y*b+z*c
  '''
  m4 = mul(inA, inB)
  return sum(setW0(m4))

def len4(inXYZW) : 
  '''
  len4([x,y,z,w]) -> sqrt(x*x+y*y+z*z+w*w)
  '''
  return math.sqrt(dot4(inXYZW, inXYZW))

def len3(inXYZW) : 
  '''
  len3([x,y,z,_]) -> sqrt(x*x+y*y+z*z)
  '''
  return math.sqrt(dot3(inXYZW, inXYZW))

def sqrLenXY(inXYZW) :
  '''
  sqrLenXY([x,y,_,_]) -> x*x + y*y
  '''
  x = getX(inXYZW)
  y = getY(inXYZW)
  return x * x + y * y
def lenXY(inXYZW) : 
  '''
  lenXY([x,y,_,_]) -> sqrt(x*x + y*y)
  '''
  return math.sqrt(sqrLenXY(inXYZW))

def sqrLenYZ(inXYZW) :
  '''
  sqrLenYZ([_,y,z,_]) -> y*y + z*z
  '''
  y = getY(inXYZW)
  z = getZ(inXYZW)
  return y * y + z * z
def lenYZ(inXYZW) : 
  '''
  lenYZ([_,y,z,_]) -> sqrt(y*y + z*z)
  '''
  return math.sqrt(sqrLenYZ(inXYZW))

def sqrLenXZ(inXYZW) :
  '''
  sqrLenXZ([x,_,z,_]) -> x*x + z*z
  '''
  x = getX(inXYZW)
  z = getZ(inXYZW)
  return x * x + z * z
def lenXZ(inXYZW) : 
  '''
  lenXZ([x,_,z,_]) -> sqrt(x*x + z*z)
  '''
  return math.sqrt(sqrLenXZ(inXYZW))

def cross3(inA, inB) : 
  '''
  cross3([x,y,z,_],[a,b,c,_]) -> [y*c - z*b, z*b - x*c, x*b - y*a, 0.0]
  '''
  tmpA = mul(inA, swizzleYZXW(inB))
  tmpB = nmsub(inB, swizzleYZXW(inA), tmpA)
  return swizzleYZXW(tmpB)

def normal4(inXYZW, err=[1.0, 0.0, 0.0, 0.0]) : 
  '''
  normal4([x,y,z,w]) -> normalized [x,y,z,w]
  '''
  dt = dot4(inXYZW, inXYZW)
  if dt < 1.0e-14 : return err
  scl = pffloat1.rsqrtClamp(dt)
  return mulScalar(inXYZW, scl)

def normal3(inXYZW, err=[1.0, 0.0, 0.0]) : 
  '''
  normal3([x,y,z,_]) -> normalized [x,y,z,_]
  '''
  dt = dot3(inXYZW, inXYZW)
  if dt < 1.0e-14 : return err
  scl = pffloat1.rsqrtClamp(dt)
  return copyW(mulScalar(inXYZW, scl), inXYZW)

def interp(inA, inB, inR) : 
  '''
  interp(a,b,r) -> (1-r)*a + r*b
  '''
  tmp = madd(inR, inB, inA)
  return nmsub(inR, inA, tmp)

def sinCosHalf(inC) : 
  '''
  sinCosHalf(cos(th)) -> [ sin(th*0.5), sin(th*0.5), sin(th*0.5), cos(th*0.5) ]
  '''
  sc = pffloat1.sinCosHalf(inC)
  return [ sc[0], sc[0], sc[0], sc[1] ]

def selectXYZW(inFalse, inTrue, inSelect) : 
  '''
  selectXYZW([x,y,z,w], [a,b,c,d], [bool0,bool1,bool3,bool4]) : [if bool0 : a else : x,...]
  '''
  tmp = list(inFalse)
  for idx in range(4) : 
    if inSelect[idx] : tmp[idx] = inTrue[idx]
  return tmp

def select(inFalse, inTrue, inSelect) : 
  '''
  select([x,y,z,w], [a,b,c,d], bool) : if bool : [a,b,c,d] else : [x,y,z,w]
  '''
  if inSelect : return list(inTrue)
  else : return list(inFalse)

def swizzleXYWZ(inXYZW) : 
  '''
  swizzleXYWZ([x,y,z,w]) : [x,y,w,z]
  '''
  return [ getX(inXYZW), getY(inXYZW), getW(inXYZW), getZ(inXYZW) ]
def swizzleXZYW(inXYZW) : 
  '''
  swizzleXZYW([x,y,z,w]) : [x,z,y,w]
  '''
  return [ getX(inXYZW), getZ(inXYZW), getY(inXYZW), getW(inXYZW) ]
def swizzleXZWY(inXYZW) : 
  '''
  swizzleXZWY([x,y,z,w]) : [x,z,w,y]
  '''
  return [ getX(inXYZW), getZ(inXYZW), getW(inXYZW), getY(inXYZW) ]
def swizzleYXWZ(inXYZW) : 
  '''
  swizzleYXWZ([x,y,z,w]) : [y,x,w,z]
  '''
  return [ getY(inXYZW), getX(inXYZW), getW(inXYZW), getZ(inXYZW) ]
def swizzleYZXW(inXYZW) : 
  '''
  swizzleYZXW([x,y,z,w]) : [y,z,x,w]
  '''
  return [ getY(inXYZW), getZ(inXYZW), getX(inXYZW), getW(inXYZW) ]
def swizzleYZWX(inXYZW) : 
  '''
  swizzleYZWX([x,y,z,w]) : [y,z,w,x]
  '''
  return [ getY(inXYZW), getZ(inXYZW), getW(inXYZW), getX(inXYZW) ]
def swizzleYWXZ(inXYZW) : 
  '''
  swizzleYWXZ([x,y,z,w]) : [y,w,x,z]
  '''
  return [ getY(inXYZW), getW(inXYZW), getX(inXYZW), getZ(inXYZW) ]
def swizzleYWZX(inXYZW) : 
  '''
  swizzleYWZX([x,y,z,w]) : [y,w,z,x]
  '''
  return [ getY(inXYZW), getW(inXYZW), getZ(inXYZW), getX(inXYZW) ]
def swizzleZXYW(inXYZW) : 
  '''
  swizzleZXYW([x,y,z,w]) : [z,x,y,w]
  '''
  return [ getZ(inXYZW), getX(inXYZW), getY(inXYZW), getW(inXYZW) ]
def swizzleZXWY(inXYZW) : 
  '''
  swizzleZXWY([x,y,z,w]) : [z,x,w,y]
  '''
  return [ getZ(inXYZW), getX(inXYZW), getW(inXYZW), getY(inXYZW) ]
def swizzleZWXY(inXYZW) : 
  '''
  swizzleZWXY([x,y,z,w]) : [z,w,x,y]
  '''
  return [ getZ(inXYZW), getW(inXYZW), getX(inXYZW), getY(inXYZW) ]
def swizzleZWYX(inXYZW) : 
  '''
  swizzleZWYX([x,y,z,w]) : [z,w,y,x]
  '''
  return [ getZ(inXYZW), getW(inXYZW), getY(inXYZW), getX(inXYZW) ]
def swizzleWXYZ(inXYZW) : 
  '''
  swizzleWXYZ([x,y,z,w]) : [w,x,y,z]
  '''
  return [ getW(inXYZW), getX(inXYZW), getY(inXYZW), getZ(inXYZW) ]
def swizzleWXZY(inXYZW) : 
  '''
  swizzleWXZY([x,y,z,w]) : [w,x,z,y]
  '''
  return [ getW(inXYZW), getX(inXYZW), getZ(inXYZW), getY(inXYZW) ]
def swizzleWYXZ(inXYZW) : 
  '''
  swizzleWYXZ([x,y,z,w]) : [w,y,x,z]
  '''
  return [ getW(inXYZW), getY(inXYZW), getX(inXYZW), getZ(inXYZW) ]
def swizzleWYZX(inXYZW) : 
  '''
  swizzleWYZX([x,y,z,w]) : [w,y,z,x]
  '''
  return [ getW(inXYZW), getY(inXYZW), getZ(inXYZW), getX(inXYZW) ]
def swizzleWZXY(inXYZW) : 
  '''
  swizzleWZXY([x,y,z,w]) : [w,z,x,y]
  '''
  return [ getW(inXYZW), getZ(inXYZW), getX(inXYZW), getY(inXYZW) ]
def swizzleWZYX(inXYZW) : 
  '''
  swizzleWZYX([x,y,z,w]) : [w,z,y,x]
  '''
  return [ getW(inXYZW), getZ(inXYZW), getY(inXYZW), getX(inXYZW) ]

def shuffleAYZW(inXYZW, inABCD) : 
  '''
  shuffleAYZW([x,y,z,w], [a,b,c,d]) : [a,y,z,w]
  '''
  return [ getX(inABCD), getY(inXYZW), getZ(inXYZW), getW(inXYZW) ]
def shuffleXBZW(inXYZW, inABCD) : 
  '''
  shuffleXBZW([x,y,z,w], [a,b,c,d]) : [x,b,z,w]
  '''
  return [ getX(inXYZW), getY(inABCD), getZ(inXYZW), getW(inXYZW) ]
def shuffleABZW(inXYZW, inABCD) : 
  '''
  shuffleABZW([x,y,z,w], [a,b,c,d]) : [a,b,z,w]
  '''
  return [ getX(inABCD), getY(inABCD), getZ(inXYZW), getW(inXYZW) ]
def shuffleXYCW(inXYZW, inABCD) : 
  '''
  shuffleXYCW([x,y,z,w], [a,b,c,d]) : [x,y,c,w]
  '''
  return [ getX(inXYZW), getY(inXYZW), getZ(inABCD), getW(inXYZW) ]
def shuffleAYCW(inXYZW, inABCD) : 
  '''
  shuffleAYCW([x,y,z,w], [a,b,c,d]) : [a,y,c,w]
  '''
  return [ getX(inABCD), getY(inXYZW), getZ(inABCD), getW(inXYZW) ]
def shuffleXBCW(inXYZW, inABCD) : 
  '''
  shuffleXBCW([x,y,z,w], [a,b,c,d]) : [x,b,c,w]
  '''
  return [ getX(inXYZW), getY(inABCD), getZ(inABCD), getW(inXYZW) ]
def shuffleABCW(inXYZW, inABCD) : 
  '''
  shuffleABCW([x,y,z,w], [a,b,c,d]) : [a,b,c,w]
  '''
  return [ getX(inABCD), getY(inABCD), getZ(inABCD), getW(inXYZW) ]
def shuffleXAZC(inXYZW, inABCD) : 
  '''
  shuffleXAZC([x,y,z,w], [a,b,c,d]) : [x,a,z,c]
  '''
  return [ getX(inXYZW), getX(inABCD), getZ(inXYZW), getZ(inABCD) ]
def shuffleYBWD(inXYZW, inABCD) : 
  '''
  shuffleYBWD([x,y,z,w], [a,b,c,d]) : [y,b,w,d]
  '''
  return [ getY(inXYZW), getY(inABCD), getW(inXYZW), getW(inABCD) ]


def alignAxisXRotateZ(inV) : 
  '''
  alignAxisXRotateZ(vec) -> ( sin, cos, vec )
  '''
  snCsLn = pffloat1.alignAxis([getX(inV), getY(inV)])
  v = setXYZ(snCsLn[2], 0.0, getZ(inV))
  return ( snCsLn[0], snCsLn[1], v )

def alignAxisXRotateY(inV) : 
  '''
  alignAxisXRotateY(vec) -> ( sin, cos, vec )
  '''
  snCsLn = pffloat1.alignAxis([getX(inV), -getZ(inV)])
  v = setXYZ(snCsLn[2], getY(inV), 0.0)
  return ( snCsLn[0], snCsLn[1], v )

def alignAxisYRotateZ(inV) : 
  '''
  alignAxisYRotateZ(vec) -> ( sin, cos, vec )
  '''
  snCsLn = pffloat1.alignAxis([getY(inV), -getX(inV)])
  v = setXYZ(0.0, snCsLn[2], getZ(inV))
  return ( snCsLn[0], snCsLn[1], v )

def alignAxisYRotateX(inV) : 
  '''
  alignAxisYRotateX(vec) -> ( sin, cos, vec )
  '''
  snCsLn = pffloat1.alignAxis([getY(inV), getZ(inV)])
  v = setXYZ(getX(inV), snCsLn[2], 0.0)
  return ( snCsLn[0], snCsLn[1], v )

def alignAxisZRotateY(inV) : #
  '''
  alignAxisZRotateY(vec) -> ( sin, cos, vec )
  '''
  snCsLn = pffloat1.alignAxis([getZ(inV), getX(inV)])
  v = setXYZ(0.0, getY(inV), snCsLn[2])
  return ( snCsLn[0], snCsLn[1], v )

def alignAxisZRotateX(inV) : 
  '''
  alignAxisZRotateX(vec) -> ( sin, cos, vec )
  '''
  snCsLn = pffloat1.alignAxis([getZ(inV), -getY(inV)])
  v = setXYZ(getX(inV), 0.0, snCsLn[2])
  return ( snCsLn[0], snCsLn[1], v )

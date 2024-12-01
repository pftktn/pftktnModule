# -*- coding: utf-8 -*-
'''
floatの操作を行う関数群

See Copyright(LICENSE.txt) for the status of this software.
 
Author: Takeharu TANIMURA <tanie@kk.iij4u.or.jp>
'''

import math

def clamp(inV, inMin, inMax) : 
  '''
  clamp(v,min,max) : min <= returnValue <= max
  '''
  return min(max(inV, inMin), inMax)


def sqrtClamp(inV) : 
  '''
  sqrtClamp(v) : sqrt(v)
  '''
  return math.sqrt(max(inV, 0.0))
def rsqrtClamp(inV) : 
  '''
  rsqrtClamp(v) : 1.0/sqrt(v)
  '''
  return 1.0 / sqrtClamp(inV)

def sinDegree(inD) : 
  '''
  sinDegree(d) : sin(radians(d))
  '''
  return math.sin(math.radians(inD))
def cosDegree(inD) : 
  '''
  cosDegree(d) : cos(radians(d))
  '''
  return math.cos(math.radians(inD))
def tanDegree(inD) : 
  '''
  tanDegree(d) : tan(radians(d))
  '''
  return math.tan(math.radians(inD))
def sinCosDegree(inD) : 
  '''
  sinCosDegree(deg) -> ( sin(deg), cos(deg) )
  '''
  return ( sinDegree(inD), cosDegree(inD) )

sinRadian = math.sin
cosRadian = math.cos
tanRadian = math.tan
def sinCosRadian(inR) : 
  '''
  sinCosDegree(rad) -> ( sin(rad), cos(rad) )
  '''
  return ( sinRadian(inR), cosRadian(inR) )

def acosRadian(inV) : 
  '''
  acosRadian(v) : acos(clamp(v, -1.0, 1.0))
  '''
  return math.acos(clamp(inV, -1.0, 1.0))
def asinRadian(inV) : 
  '''
  asinRadian(v) : asin(clamp(v, -1.0, 1.0))
  '''
  return math.asin(clamp(inV, -1.0, 1.0))
atanRadian = math.atan
atan2Radian = math.atan2

def acosDegree(inV) : 
  '''
  acosDegree(v) : degrees(acos(clamp(v, -1.0, 1.0)))
  '''
  return math.degrees(acosRadian(inV))
def asinDegree(inV) : 
  '''
  asinDegree(v) : degrees(asin(clamp(v, -1.0, 1.0)))
  '''
  return math.degrees(asinRadian(inV))
def atanDegree(inV) : 
  '''
  atanDegree(v) : degrees(atan(v))
  '''
  return math.degrees(math.atan(inV))
def atan2Degree(inY, inX) : 
  '''
  atan2Degree(y,x) : degrees(atan2(y,x))
  '''
  return math.degrees(math.atan2(inY, inX))


def sinCosHalf(inC) : 
  '''
  sinCosHalf(cos(th)) -> [ sin(0.5*th), cos(0.5*th) ]
  '''
  cs = clamp(inC, -1.0, 1.0)
  hSn = sqrtClamp(0.5 - 0.5 * cs)
  hCs = sqrtClamp(0.5 * cs + 0.5)
  return ( hSn, hCs )

def isNanInf(inV) : 
  '''
  isNanInf(v) : isnan(v) or isinf(v)
  '''
  if math.isnan(inV) or math.isinf(inV) : return True
  else : return False

def alignAxis(inUV) : 
  '''
  alignAxis([u,v]) : [sin,cos,uvLen]
  '''
  uvLen = sqrtClamp(inUV[0] * inUV[0] + inUV[1] * inUV[1])
  result = [ 0.0, 1.0, uvLen ]
  if uvLen > 1.0e-10 : 
    scl = 1.0 / uvLen
    result[0] = inUV[1] * scl
    result[1] = inUV[0] * scl
  return result

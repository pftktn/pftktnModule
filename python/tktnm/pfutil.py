# -*- coding: utf-8 -*-
'''
雑多なもの

See Copyright(LICENSE.txt) for the status of this software.
 
Author: Takeharu TANIMURA <tanie@kk.iij4u.or.jp>
'''


import enum


def isUnique(inLst, inObj) :
  for elm in inLst :
    if elm is inObj :
      return False
  return True

def appendUnique(ioLst, inObj) :
  if isUnique(ioLst, inObj) :
    ioLst.append(inObj)
    return True
  else :
    return False


def insertUnique(ioLst, inIdx, inObj) :
  if isUnique(ioLst, inObj) :
    ioLst.insert(inIdx, inObj)
    return True
  else :
    return False


def insertBefore(ioLst, inTgt, inObj) :
  if inTgt is not None :
    for idx, elm in enumerate(ioLst) :
      if elm is inTgt :
        ioLst.insert(idx, inObj)
        return
  ioLst.append(inObj)


class pfSortedList(object) :
  '''
  ソート済みリストクラス
  '''
  __list = None  # list。ソート済みのリスト
  @property
  def List(self) : 
    '''
    List : list. ソート済みのリストの取得。
    '''
    return self.__list
  __getKeyFunc = None  # リスト内のオブジェクトから、キーを取得する関数。
  @staticmethod
  def defaultGetKeyFunc(inV) : 
    '''
    defaultGetKeyFunc(str) : 特に指定がない場合用のgetKeyFunc。
    '''
    return inV
  def __init__(self, getKeyFunc=None) :
    '''
    コンストラクタ
    '''
    self.__list = list()
    if getKeyFunc is None :
      self.__getKeyFunc = pfSortedList.defaultGetKeyFunc
    else :
      self.__getKeyFunc = getKeyFunc
  
  def getIndex(self, inV) :
    '''
    getIndex(object) : int. オブジェクトを渡してインデックスの取得
    '''
    return self.getIndexByKey(self.__getKeyFunc(inV))

  def getIndexByKey(self, inK) :
    '''
    getIndexByKey(str) : int. キーを渡してインデックスの取得。存在しないキーの場合は-1
    '''
    minIdx = 0
    maxIdx = len(self.__list) - 1
    while minIdx <= maxIdx : 
      cnt = maxIdx - minIdx + 1
      if cnt < 5 :
        for idx in range(cnt) :
          k = self.__getKeyFunc(self.__list[minIdx + idx])
          if k == inK : return minIdx + idx
        return -1
      else :
        idx = (minIdx + maxIdx) // 2
        k = self.__getKeyFunc(self.__list[idx])
        if k == inK : return idx
        if k < inK : minIdx = idx + 1
        else : maxIdx = idx - 1
    return -1

  def getValueByKey(self, inK) :
    '''
    getValueByKey(str) : 
    '''
    idx = self.getIndexByKey(inK)
    if idx >= 0 : return self.__list[idx]
    else : return None

  def addValue(self, inV) :
    '''
    addValue(object) : int. オブジェクトの追加。
    '''
    vKey = self.__getKeyFunc(inV)
    idx = self.getIndexByKey(vKey)
    if idx >= 0 : return None
    minIdx = 0
    maxIdx = len(self.__list) - 1
    if maxIdx < 0 : 
      self.__list.append(inV)
      return 0
    while minIdx <= maxIdx : 
      cnt = maxIdx - minIdx + 1
      if cnt < 5 :
        for idx in range(cnt) :
          k = self.__getKeyFunc(self.__list[minIdx + idx])
          if k > vKey : 
            self.__list.insert(minIdx + idx, inV)
            return minIdx + idx
        self.__list.insert(minIdx + cnt, inV)
        return minIdx + cnt
      else :
        idx = (minIdx + maxIdx) // 2
        k = self.__getKeyFunc(self.__list[idx])
        if k < vKey : minIdx = idx + 1
        else : maxIdx = idx - 1
    return -1

  def delValue(self, inV) :
    '''
    delValue(object) : object. オブジェクトを指定してリストから削除する。
    '''
    return self.delValueByKey(self.__getKeyFunc(inV))

  def delValueByKey(self, inK) :
    '''
    delValueByKey(str) : object. キーを指定してリストからオブジェクトを削除する。
    '''
    idx = self.getIndexByKey(inK)
    if idx >= 0 : return self.__list.pop(idx)
    return None

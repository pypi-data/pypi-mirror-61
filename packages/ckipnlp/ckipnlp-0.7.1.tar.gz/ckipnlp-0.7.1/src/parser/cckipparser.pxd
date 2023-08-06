# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'CC BY-NC-SA 4.0'

cdef extern:

	ctypedef void* corenlp_t

	corenlp_t CKIPCoreNLP_New()
	int CKIPCoreNLP_InitData(corenlp_t obj, char *FileName);
	int CKIPCoreNLP_ApplyFile(corenlp_t obj, char *input, char *output);
	int CKIPCoreNLP_ApplyList(corenlp_t obj, int length, const Py_UNICODE **inputList);
	int CKIPCoreNLP_Parse(corenlp_t obj, const Py_UNICODE* pwsText, Py_UNICODE** ppwsResult);
	int CKIPCoreNLP_ParseFile(corenlp_t obj, char *input, char *output);
	const Py_UNICODE* CKIPCoreNLP_GetResultBegin(corenlp_t obj);
	const Py_UNICODE* CKIPCoreNLP_GetResultNext(corenlp_t obj);
	void CKIPCoreNLP_Destroy(corenlp_t obj);

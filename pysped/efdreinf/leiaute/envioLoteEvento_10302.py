
# -*- coding: utf-8 -*-
#
# PySPED - Python libraries to deal with Brazil's SPED Project
#
# Copyright (C) 2010-2012
# Copyright (C) Wagner Pereira <wagner.pereira at tauga.com.br>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation, either version 2.1 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# PySPED - Bibliotecas Python para o
#          SPED - Sistema Público de Escrituração Digital
#
# Copyright (C) 2010-2012
# Copyright (C) Aristides Caldeira <aristides.caldeira arroba tauga.com.br>
#
# Este programa é um software livre: você pode redistribuir e/ou modificar
# este programa sob os termos da licença GNU Library General Public License,
# publicada pela Free Software Foundation, em sua versão 2.1 ou, de acordo
# com sua opção, qualquer versão posterior.
#
# Este programa é distribuido na esperança de que venha a ser útil,
# porém SEM QUAISQUER GARANTIAS, nem mesmo a garantia implícita de
# COMERCIABILIDADE ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. Veja a
# GNU Library General Public License para mais detalhes.
#
# Você deve ter recebido uma cópia da GNU Library General Public License
# juntamente com este programa. Caso esse não seja o caso, acesse:
# <http://www.gnu.org/licenses/>
#

from __future__ import (division, print_function, unicode_literals,
                        absolute_import)

from builtins import str
import os
import base64
from reportlab.graphics.barcode import createBarcodeDrawing
from genshi.core import Markup
from pysped.xml_sped import *
from pysped.efdreinf.leiaute import ESQUEMA_ATUAL_VERSAO_1 as ESQUEMA_ATUAL

PYBRASIL = False
#try:
from pybrasil.inscricao import formata_ie
from pybrasil.telefone import formata_fone
PYBRASIL = True
#except:
    #pass

DIRNAME = os.path.dirname(__file__)

NAMESPACE_LOTE_EFDREINF = 'http://www.reinf.esocial.gov.br/schemas/envioLoteEventos/v1_03_02'


class Evento(XMLNFe):
    def __init__(self):
        super(Evento, self).__init__()
        self.Id = TagCaracter(nome='evento', propriedade='Id', raiz='//Reinf/loteEventos/evento', namespace=NAMESPACE_LOTE_EFDREINF, namespace_obrigatorio=False)
        self.eventos = []

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += '<loteEventos>'
                
        for e in self.eventos:
            xml += '<evento id="' + e.id_evento + '">'
            xml += e.xml
            xml += '</evento>'                     
            
        xml += '</loteEventos>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):            
            self.Id.xml = arquivo
            self.eventos.xml = arquivo
            
    xml = property(get_xml, set_xml)


class LoteEventoEFDReinf(XMLNFe):
    def __init__(self):
        super(LoteEventoEFDReinf, self).__init__()
        self.envioLoteEventos = Evento()
        self.caminho_esquema = os.path.join(DIRNAME, 'schema/', ESQUEMA_ATUAL + '/')
        self.arquivo_esquema = 'EnvioLoteEventos.xsd'
        self.id_evento = ''

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        #xml += ABERTURA
        xml += '<Reinf xmlns="' + NAMESPACE_LOTE_EFDREINF + '">'
        xml += self.envioLoteEventos.xml
        xml += '</Reinf>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.envioLoteEventos.xml = arquivo
    
    xml = property(get_xml, set_xml)

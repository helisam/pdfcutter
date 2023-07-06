import os
import random
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime
from os.path import basename

from PyPDF2 import PdfWriter, PdfReader
from flask import Flask, request, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

import models.enum.tipo_enum as Tipo

root = "C:\\TEMP"

app = Flask(__name__)
CORS(app)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uploads.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)


@dataclass
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    path = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(25), nullable=False)
    user = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['GET'])
def index():
    return "Hello Flask!"


@app.route("/api/v1/upload", methods=['POST'])
def upload_pdf():
    if request.method == 'POST':
        # This will be executed on POST request.
        arquivo = request.files['file']
        if not arquivo:
            return 'No file uploaded.'

        if arquivo.content_type != 'application/pdf':
            return

        content = PdfReader(arquivo)

        root_new = root + '\\' + datetime.utcnow().strftime('%d-%m-%Y--%H-%M-%S')

        is_exist = os.path.exists(root_new)

        if not is_exist:
            # Create a new directory because it does not exist
            os.makedirs(root_new)
            print("The new directory is created!")

        if len(content.pages) > 0:
            for page in range(len(content.pages)):
                page_obj = content.pages[page]
                text = page_obj.extract_text()
                if 'PIX' in text:
                    nome_creditado = fill_nome_creditado(Tipo.Tipo.PIX, text)
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.PIX, text)
                    identificacao_comprovante = fill_identificacao_comprovante(
                        Tipo.Tipo.PIX, text)

                    output_filename = save_splitted_document(Tipo.Tipo.PIX,
                                                             identificacao_comprovante,
                                                             nome_creditado, page_obj,
                                                             valor_creditado, root_new)
                    print('Created: {}'.format(output_filename))
                elif 'boleto' in text:
                    nome_creditado = fill_nome_creditado(Tipo.Tipo.BOLETO, text)
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.BOLETO, text)

                    output_filename = save_splitted_document(Tipo.Tipo.BOLETO, None,
                                                             nome_creditado, page_obj,
                                                             valor_creditado, root_new)
                    print('Created: {}'.format(output_filename))
                elif 'conta corrente' in text:
                    nome_creditado = fill_nome_creditado(Tipo.Tipo.CC, text)
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.CC, text)

                    output_filename = save_splitted_document(Tipo.Tipo.CC, None,
                                                             nome_creditado, page_obj,
                                                             valor_creditado, root_new)
                    print('Created: {}'.format(output_filename))
                elif 'DARF' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.DARF, text)

                    output_filename = save_splitted_document(Tipo.Tipo.DARF, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'VIVO' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.VIVO, text)

                    output_filename = save_splitted_document(Tipo.Tipo.VIVO, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'Tributos Estaduais' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.TRIB_ESTADUAL_S_BARRA, text)

                    output_filename = save_splitted_document(Tipo.Tipo.TRIB_ESTADUAL_S_BARRA, None,
                                                             None, page_obj,
                                                             valor_creditado, root_new)
                    print('Created: {}'.format(output_filename))
                elif 'Tributos Municipais' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.TRIB_MUNICIPAL, text)

                    output_filename = save_splitted_document(Tipo.Tipo.TRIB_MUNICIPAL, None,
                                                             None, page_obj,
                                                             valor_creditado, root_new)
                    print('Created: {}'.format(output_filename))
                elif 'GRRF' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.GRRF, text)

                    output_filename = save_splitted_document(Tipo.Tipo.GRRF, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'TED C' in text:
                    nome_creditado = fill_nome_creditado(Tipo.Tipo.TED, text)
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.TED, text)

                    output_filename = save_splitted_document(Tipo.Tipo.TED, None,
                                                             nome_creditado, page_obj,
                                                             valor_creditado, root_new)
                    print('Created: {}'.format(output_filename))
                elif 'GPS' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.GPS, text)

                    output_filename = save_splitted_document(Tipo.Tipo.GPS, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'SABESP' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.SABESP, text)

                    output_filename = save_splitted_document(Tipo.Tipo.SABESP, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'ALGAR' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.ALGAR, text)

                    output_filename = save_splitted_document(Tipo.Tipo.ALGAR, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'GRF' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.GRF, text)

                    output_filename = save_splitted_document(Tipo.Tipo.GRF, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'GARE' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.GARE, text)

                    output_filename = save_splitted_document(Tipo.Tipo.GARE, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'DARE' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.SEFAZ_DARE, text)

                    output_filename = save_splitted_document(Tipo.Tipo.SEFAZ_DARE, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'CLARO S.A.' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.CLARO, text)

                    output_filename = save_splitted_document(Tipo.Tipo.CLARO, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                elif 'ELETROPAULO' in text:
                    valor_creditado = fill_valor_creditado(Tipo.Tipo.ELETROPAULO, text)

                    output_filename = save_splitted_document(Tipo.Tipo.ELETROPAULO, None, None,
                                                             page_obj, valor_creditado,
                                                             root_new)
                    print('Created: {}'.format(output_filename))
                else:
                    output_filename = save_splitted_document(Tipo.Tipo.NAO_MAPEADO, None, None,
                                                             page_obj, None, root_new)
                    print('Created: {}'.format(output_filename))
        else:
            pass

        print(content.pages)
        page_obj = content.pages[0]
        print(page_obj.extract_text())

        upload = Upload(file_name=arquivo.filename,
                        path=root_new,
                        status='OK',
                        user='Marine.geology.student')

        # db.session.add(upload)
        # db.session.commit()

        # uploads: List[Upload] = Upload.query.all()

        # json_string: str = orjson.dumps(uploads, option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY).decode('utf-8')

        # create a ZipFile object
        with zipfile.ZipFile('{}.zip'.format(root_new), 'w') as zipfolder:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(root_new):
                for filename in filenames:
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipfolder.write(filePath, basename(filePath))
            # zipfolder.close()

        try:
            with open('{}.zip'.format(root_new), 'rb') as f:
                data = f.readlines()

            f.close()
        # os.remove('{}.zip'.format(root_new))

            return Response(data,
                            mimetype='application/zip',
                            headers={'Content-Disposition': 'attachment;filename={}.zip'.format(root_new)})

        except Exception as e:
            return str(e)
        finally:
            os.remove('{}.zip'.format(root_new))

        # return Response(
        #     message=f"Adicionado com sucesso.",
        #     category="success",
        #     data=json_string,
        #     status=200,
        #     headers={'Content-Disposition': 'attachment;{}'.format(root_new)}
        # )


def save_splitted_document(tipo, identificacao_comprovante, nome_creditado,
                           page_obj, valor_creditado, root_new):
    pdf_writer = PdfWriter()
    pdf_writer.add_page(page_obj)
    output_filename = ''
    if tipo == Tipo.Tipo.PIX:
        # output_filename = '{}-{}-{}-{}-{}.pdf'.format(type, nome_creditado, valor_creditado, identificacao_comprovante, page + 1)
        output_filename = '{}-{}-{}-{}.pdf'.format(tipo.value,
                                                   nome_creditado.title(),
                                                   valor_creditado,
                                                   identificacao_comprovante)
    if tipo == Tipo.Tipo.BOLETO or tipo == Tipo.Tipo.CC or tipo == Tipo.Tipo.TED:
        output_filename = '{}-{}-{}.pdf'.format(tipo.value, nome_creditado.title(),
                                                valor_creditado)
    if tipo == Tipo.Tipo.DARF or tipo == Tipo.Tipo.VIVO or tipo == Tipo.Tipo.TRIB_ESTADUAL_S_BARRA or tipo == Tipo.Tipo.GRRF or tipo == Tipo.Tipo.GPS or tipo == Tipo.Tipo.SABESP or tipo == Tipo.Tipo.ALGAR or tipo == Tipo.Tipo.TRIB_MUNICIPAL or tipo == Tipo.Tipo.GRF or tipo == Tipo.Tipo.GARE or tipo == Tipo.Tipo.SEFAZ_DARE or tipo == Tipo.Tipo.CLARO or tipo == Tipo.Tipo.ELETROPAULO:
        output_filename = '{}-{}.pdf'.format(tipo.value, valor_creditado)
    if tipo == Tipo.Tipo.NAO_MAPEADO:
        output_filename = '{}-{}.pdf'.format(tipo.value, ([random.randint(1, 10000) for _ in range(1)]))
    complete_name = os.path.join(root_new, output_filename)
    with open(complete_name, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
    return output_filename


def fill_identificacao_comprovante(tipo, text):
    if tipo == Tipo.Tipo.PIX:
        return re.search(r'(?<=identificação no comprovante:)(.*)(?=\n)',
                         text).group(1).lstrip().rstrip()


def fill_valor_creditado(tipo, text):
    if tipo == Tipo.Tipo.PIX or tipo == Tipo.Tipo.SEFAZ_DARE:
        return re.search(r'(?<=Valor:|valor:)(.*)(?=\n)',
                         text).group(1).lstrip().rstrip()
    if tipo == Tipo.Tipo.BOLETO:
        return re.search(
            r'(?<=Valor do boleto \(R\$\);)(\n|.)*?(?=\(-\) Desconto)',
            text).group(0).rstrip().lstrip().replace('\n', '')
    if tipo == Tipo.Tipo.CC:
        return re.search(r'(?<=Valor:)(.*)(?=\n)', text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.DARF:
        return re.search(r'(?<=valor total:)(.*)(?=\n)',
                         text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.VIVO or tipo == Tipo.Tipo.TRIB_ESTADUAL_S_BARRA or tipo == Tipo.Tipo.CLARO or tipo == Tipo.Tipo.ELETROPAULO:
        return re.search(r'(?<=Valor do documento:)(.*)(?=\n)',
                         text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.GRRF:
        return re.search(r'(?<=valor recolhido:)(.*)(?=\n)',
                         text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.TED:
        return re.search(r'(?<=Valor da TED:)(.*)(?=\n)',
                         text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.GPS:
        return re.search(r'(?<=valor total:)(.*)(?=\n)',
                         text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.SABESP or tipo == Tipo.Tipo.ALGAR or tipo == Tipo.Tipo.TRIB_MUNICIPAL:
        return re.search(
            r'(?<=Valor do documento: R\$ )(\n|.)*?(?=\n)',
            text).group(0).rstrip().lstrip().replace('\n', '')
    if tipo == Tipo.Tipo.GRF:
        return re.search(
            r'(?<=Valor Recolhido: R\$ )(\n|.)*?(?=\n)',
            text).group(0).rstrip().lstrip().replace('\n', '')
    if tipo == Tipo.Tipo.GARE:
        return re.search(
            r'(?<=VALOR TOTAL  )(\n|.)*?(?=  \n)',
            text).group(0).rstrip().lstrip().replace('\n', '')

def fill_nome_creditado(tipo, text):
    if tipo == Tipo.Tipo.PIX:
        return re.search(r'(?<=nome do recebedor:)(.*)(?=\n)',
                         text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.BOLETO:
        return re.search(r'(?<=Beneficiário:)(.*)(?=CPF)',
                         text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.CC:
        return re.search(r'(?<=Nome:)(.*)(?=\n)', text).group(1).rstrip().lstrip()
    if tipo == Tipo.Tipo.TED:
        return re.search(r'(?<=Nome do favorecido:)(.*)(?=\n)',
                         text).group(1).rstrip().lstrip()


if __name__ == '__main__':
    app.run("0.0.0.0")

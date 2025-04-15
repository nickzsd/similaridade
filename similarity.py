from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import pandas as pd

app = Flask(__name__)
CORS(app)

BooksExcel = pd.read_excel('Similaridade.xlsx')
books      = BooksExcel.to_dict(orient='records')

class Similarity_Books:    
    booksCount = 0

    gender_mapping = {
            1: 'Ação',
            2: 'Autoajuda',
            3: 'Comédia',
            4: 'Culinária',
            5: 'Estudos',
            6: 'Finanças',
            7: 'Infantil',
            8: 'Mistério',
            9: 'Psicologia',
            10: 'Religião',
            11: 'Romance',
            12: 'Suspense',
            13: 'Técnico',
            14: 'Terror',
            15: 'Aventura'
        }
    Rate_mapping_Calc = {
        2:  10,
        3:  12,
        4:  14,
        5:  16,
        6:  18
    }
    Rate_mapping = {
        1: 'Livre',
        2:  10,
        3:  12,
        4:  14,
        5:  16,
        6:  18
    }
    
    @staticmethod
    def getSimilarsGenders(_gender: int) -> str:
        Filtered_Similars = ""
        if _gender == 1: #ação
            Filtered_Similars = '1,12,15'
        if _gender == 12 or _gender == 14:  # Suspense, Terror
            Filtered_Similars = '12,14' if _gender == 12 else \
                                '14,12'
        elif _gender == 3 or _gender == 11:  # Comédia, Romance
            Filtered_Similars = '3,11' if _gender == 3 else '11,3'
        elif _gender == 2 or _gender == 9:  # Autoajuda, Psicologia
            Filtered_Similars = '2,9' if _gender == 2 else '9,2'
        elif _gender == 4 or _gender == 5:  # Culinária, Estudos
            Filtered_Similars = '4,5' if _gender == 4 else '5,4'
        elif _gender == 6:  # Finanças / estudos
            Filtered_Similars = '6,5'
        elif _gender == 7:  # Infantil
            Filtered_Similars = '7'
        elif _gender == 8:  # Mistério
            Filtered_Similars = '8,12'
        elif _gender == 10:  # Religião
            Filtered_Similars = '10,13'
        elif _gender == 13:  # Técnico
            Filtered_Similars = '13,9,10,4,6'
        elif _gender == 15: #Aventura
            Filtered_Similars = '15,1,11'
        return Filtered_Similars
    
    @staticmethod
    def makeConsult(_type: int, _info: str) -> list:
        Selections = []        
        for _refbook in books: #Primeira busca com todos os livros 
            AppendBook = False        
            if(_type == 1):
                _refbook_Genderidx  = _refbook['Genero']
                AppendBook  = True if any(letter in _refbook_Genderidx for letter in _info) else False
            elif(_type == 2):
                AppendBook  =  True if (_refbook['Classificação Indicativa'] == Similarity_Books.Rate_mapping[int(_info)]) else False
            elif(_type == 3):
                AppendBook  =  True if (_refbook['Paginas'] >= int(_info)) else False
            elif(_type == 4):
                RefbookInfo = str(_refbook['Autor']).lower()
                _info       = _info.lower()                    
                AppendBook  =  True if (_info in RefbookInfo) else False 
            elif(_type == 5):
                RefbookInfo = str(_refbook['Titulo']).lower()
                _info       = _info.lower()
                AppendBook  =  True if (_info in RefbookInfo) else False
            elif(_type == 6):
                var1 = str(_refbook['Classificação']).replace(",", ".")
                var2 = str(_info).replace(",", ".")                
                AppendBook  =  True if float(var1) >= float(var2) else False
                
            if(AppendBook == True):
                Selections.append(_refbook)

        target_rating = float(_info.replace(',', '.')) if _type == 6 else None

        if _type == 1:
            Selections = sorted(
                Selections,
                key=lambda x: (
                    abs(float(str(x['Classificação']).replace(',', '.')) - target_rating) if target_rating is not None else 0,
                    -float(str(x['Classificação']).replace(',', '.')),
                    x['Genero'] != str(_info[0])
                )
            )
        elif _type == 2:
            Selections = sorted(
                Selections,
                key=lambda x: (
                    abs(float(str(x['Classificação']).replace(',', '.')) - target_rating) if target_rating is not None else 0,
                    -float(str(x['Classificação']).replace(',', '.')),
                    x['Classificação Indicativa'] != Similarity_Books.Rate_mapping[int(_info)]
                )
            )  
        elif _type == 3:
            min_pag = int(_info)
            Selections = sorted(
                Selections,
                key=lambda x: (
                    abs(float(str(x['Classificação']).replace(',', '.')) - target_rating) if target_rating is not None else 0,
                    -float(str(x['Classificação']).replace(',', '.')),
                    abs(x['Paginas'] - min_pag)
                )
            )
        else:
            Selections = sorted(
                Selections,
                key=lambda x: (
                    abs(float(str(x['Classificação']).replace(',', '.')) - target_rating) if target_rating is not None else 0,
                    -float(str(x['Classificação']).replace(',', '.'))
                )
            )     
        return Selections;

    @staticmethod
    def MakeMistConsult(MistInfo: dict) -> list:
        Selections = []
        attempts   = 0

        if 6 in MistInfo:
            RateLimit = int(MistInfo[6]) 

        if 3 in MistInfo:
            PageLimit  = int(MistInfo[3])

        if 2 in MistInfo:
            _MainAge = int(MistInfo[2])

        if 1 in MistInfo:
            _Genderinfo = ','.join(MistInfo[1])     

        while len(Selections) < Similarity_Books.booksCount:
            print(f'Info = {MistInfo}')

            for _refbook in books:         
                valid = True

                if 1 in MistInfo: #genero
                    _refbook_Genderidx = str(_refbook['Genero'])
                    print(f"{_refbook_Genderidx} // {_Genderinfo}")
                    if any(g in _refbook_Genderidx for g in _Genderinfo):
                        print("possui")
                    else:
                        valid = False

                if 2 in MistInfo:  # Classificação indicativa
                    if _refbook['Classificação Indicativa'] != Similarity_Books.Rate_mapping[MistInfo[2]]:
                        valid = False

                if 3 in MistInfo:  # Número de páginas (mínimo)
                    if _refbook['Paginas'] < int(MistInfo[3]):
                        valid = False

                if 4 in MistInfo:  # Autor
                    RefbookInfo = str(_refbook['Autor']).lower()
                    _info       = str(MistInfo[4]).lower()
                    if _info not in RefbookInfo:
                        valid = False

                if 5 in MistInfo:  # Título
                    RefbookInfo = str(_refbook['Titulo']).lower()
                    _info       = str(MistInfo[5]).lower()
                    if _info not in RefbookInfo:
                        valid = False
                
                if 6 in MistInfo:  # Nota (Minima)
                    var1 = str(_refbook['Classificação']).replace(",", ".")
                    var2 = str(MistInfo[6]).replace(",", ".")                    
                    if float(var1) < float(var2):
                        valid = False
                
                if valid:  
                    Selections.append(_refbook)

            attempts = attempts + 1

            if attempts == 10:
                break

            if(len(Selections) > (Similarity_Books.booksCount + 1)):
                break;  

            if(len(Selections) < (Similarity_Books.booksCount + 1)):
                if 3 in MistInfo: MistInfo[3] = (int(MistInfo[3]) * 0.80) 
                if 2 in MistInfo: MistInfo[2] = (MistInfo[2] - 1) if (MistInfo[2] != 1) else MistInfo[2]                        

        if 1 in MistInfo:
            _Genderinfo = _Genderinfo.split(',')[0]
            Selections = sorted(
                Selections,
                key=lambda x: (
                    x['Genero'] != _Genderinfo,  # Prioriza livros com o primeiro gênero
                    abs(float(str(x['Classificação']).replace(',', '.')) - float(str(MistInfo[6]).replace(',', '.'))) if 6 in MistInfo else 0,
                    -float(str(x['Classificação']).replace(',', '.')) 
                )
            )
        elif 2 in MistInfo:
            Selections = sorted(
                Selections,
                key=lambda x: (
                    abs(float(str(x['Classificação']).replace(',', '.')) - float(str(MistInfo[6]).replace(',', '.'))) if 6 in MistInfo else 0,
                    -float(str(x['Classificação']).replace(',', '.')),
                    x['Classificação Indicativa'] == Similarity_Books.Rate_mapping[_MainAge]
                )
            )
        elif 3 in MistInfo:            
            Selections = sorted(
                Selections,
                key=lambda x: (
                    abs(float(str(x['Classificação']).replace(',', '.')) - float(str(MistInfo[6]).replace(',', '.'))) if 6 in MistInfo else 0,
                    -float(str(x['Classificação']).replace(',', '.')),
                    abs(x['Paginas'] - PageLimit)
                )
            )                
        else:
            Selections = sorted(
                Selections,
                key=lambda x: (
                    abs(float(str(x['Classificação']).replace(',', '.')) - float(str(MistInfo[6]).replace(',', '.'))) if 6 in MistInfo else 0,
                    -float(str(x['Classificação']).replace(',', '.'))
                )
            )

        return Selections
            
    def FilterType(FilterType_Int: int,_Info: dict) -> list:     
        '''Escopo basico
        1 = genero
        2 = Classificação
        3 = Numero de Paginas
        4 = Autor
        5 = Nome do Livro
        6 = Nota
        '''        
        if(FilterType_Int == 1):            
            for key,value in _Info.items():            
                return Similarity_Books.makeConsult(int(key),value)
        elif(FilterType_Int == 2):
            MistInfo = {}            
            for key,value in _Info.items():            
                MistInfo[int(key)] = (value)            

            return Similarity_Books.MakeMistConsult(MistInfo)        

    @staticmethod
    def get_key(genre_name: str) -> int:        
        genre_name = genre_name.lower()
                
        gender_key = {v.lower(): k for k, v in Similarity_Books.gender_mapping.items()}
                
        for key,value in gender_key.items():
            if(key == genre_name):  
                _key = value         
        
        return _key

@app.route('/get_Books', methods=['POST'])
def get_Books():
    data            = request.json
    ListInfo        = data.get('_Info')
    BookSelection   = []
    FilterSelection = []

    if not ListInfo:
        return jsonify({"error": "No genre provided"}), 400  

    print(f'key: {ListInfo[0]} / value: {ListInfo[1]} / Count: {ListInfo[2]}')      

    Similarity_Books.booksCount = int(ListInfo[2])
    BookSelection = Similarity_Books.FilterType(ListInfo[0],ListInfo[1])

    FilterSelection = BookSelection[:((int(ListInfo[2]) + 1) if len(BookSelection) > (int(ListInfo[2]) + 1) else len(BookSelection))]    

    print(f'{FilterSelection}\n\nTOTAL:{len(FilterSelection)}')

    return jsonify({"key": FilterSelection})

@app.route('/get_gender_key', methods=['POST'])
def get_gender_key():
    data       = request.json
    genre_name = data.get('genre') 

    if not genre_name:
        return jsonify({"error": "No genre provided"}), 400

    key = Similarity_Books.get_key(genre_name[0]) 

    print(key) 
    
    if key is None:
        return jsonify({"error": "Genre not found"}), 404
    
    SimilarGender = Similarity_Books.getSimilarsGenders(key)    
    SimilarGender = [int(num) for  num in SimilarGender.split(',')]
    Gender_List = [Similarity_Books.gender_mapping[idx] for idx in SimilarGender]    

    print(Gender_List)

    return jsonify({"key": Gender_List}) 

@app.route("/CheckServer", methods=["GET"])
def home():
    return "Server is running", 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
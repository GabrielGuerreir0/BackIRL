import enum

class StatusFrequencia(str, enum.Enum):
    presente = "presente"
    ausente = "ausente"
    justificado = "justificado"

# ADICIONE ESTE NOVO ENUM
class EnumSituacao(str, enum.Enum):
    satisfatorio = "Satisfatório"
    atencao = "Atenção"
    insatisfatorio = "Insatisfatório"
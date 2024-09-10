import pandas as pd
from database.connect_db import ConnectDataBase

class DatabaseQueries:
    def __init__(self):
        self.db = ConnectDataBase()

    def execute_query(self, query, params=None):
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()
        return pd.DataFrame(data, columns=columns)

    
    # TABELAS *
    def get_all_cameras(self):
        query = "SELECT * FROM cameras"
        return self.execute_query(query)

    def get_all_dvrs(self):
        query = "SELECT * FROM dvrs"
        return self.execute_query(query)
    
    def get_all_categorias_status(self):
        query = "SELECT * FROM categorias_status"
        return self.execute_query(query)
    
    def get_all_relatorio_mestre(self):
        query_mestre = """
        SELECT * FROM relatorio_mestre
        """
        return self.execute_query(query_mestre)
    
    def get_all_relatorio_diario_cameras(self):
        query_cameras = """
        SELECT * FROM relatorio_diario_cameras
        """
        return self.execute_query(query_cameras)
    
    def get_all_relatorio_diario_dvrs(self):
        query_dvrs = """
        SELECT * FROM relatorio_diario_dvrs
        """
        return self.execute_query(query_dvrs)

    # Obtém a latitude e longitude das câmeras
    def get_latitude_and_longitude_cameras(self):
        query = """
        SELECT camera_nome, camera_lat, camera_long FROM cameras
        WHERE camera_lat IS NOT NULL AND camera_long IS NOT NULL AND camera_nome != 'Vago';
        """
        return self.execute_query(query)
    
    # Função para obter as câmeras com o nome do DVR correspondente
    def get_cameras_with_dvr(self):
        query = """
        SELECT c.camera_id, c.camera_nome, d.dvr_nome
        FROM cameras c
        JOIN dvrs d ON c.dvr_id = d.dvr_id
        ORDER BY d.dvr_nome, c.camera_id
        """
        return self.execute_query(query)
    
    # Obtém as datas preenchidas do reletório
    def get_available_dates(self):
        query = "SELECT relatorio_data FROM relatorio_mestre ORDER BY relatorio_data DESC"
        df = self.execute_query(query)
        return df['relatorio_data'].tolist()
    
    # 
    def get_query_cameras(self):
        query_cameras = """
        SELECT c.camera_nome, c.dvr_id, c.camera_lat, c.camera_long, cs.categoria_status_nome AS relatorio_camera_status, c.camera_id
        FROM relatorio_diario_cameras rdc
        JOIN cameras c ON rdc.camera_id = c.camera_id
        JOIN categorias_status cs ON rdc.categoria_status_id = cs.categoria_status_id
        JOIN relatorio_mestre rm ON rdc.idrelatorio_mestre = rm.idrelatorio_mestre
        """
        return self.execute_query(query_cameras)

    # 
    def get_query_dvrs(self):
        query_dvrs = """
        SELECT d.dvr_id, d.dvr_nome, cs.categoria_status_nome AS relatorio_dvr_status, d.dvr_modelo, d.dvr_marca, d.dvr_ip
        FROM relatorio_diario_dvrs rdd
        JOIN dvrs d ON rdd.dvr_id = d.dvr_id
        JOIN categorias_status cs ON rdd.categoria_status_id = cs.categoria_status_id
        JOIN relatorio_mestre rm ON rdd.idrelatorio_mestre = rm.idrelatorio_mestre
        """
        return self.execute_query(query_dvrs)

    # Atualizando o nome da câmera no banco de dados
    def update_camera_name(self, camera_id, new_name):
        query = "UPDATE cameras SET camera_nome = %s WHERE camera_id = %s"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (new_name, camera_id))

    # Atualizando a resolucao da câmera
    def update_camera_resolution(self, camera_id, new_resolution):
        query = "UPDATE cameras SET camera_resolucao = %s WHERE camera_id = %s"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (new_resolution, camera_id))
    
    # Atualizando a URL da câmera
    def update_camera_url(self, camera_id, new_url):
        query = "UPDATE cameras SET camera_url = %s WHERE camera_id = %s"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (new_url, camera_id))
    
    # Atualizando a Latitude e Longitude da câmera
    def update_camera_lat_long(self, camera_id, new_camera_lat, new_camera_long):
        query = "UPDATE cameras SET camera_lat = %s, camera_long = %s WHERE camera_id = %s"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (new_camera_lat, new_camera_long, camera_id))
    
    # Atualizando o DVR da câmera
    def update_camera_dvr(self, camera_id, new_dvr):
        query = "UPDATE cameras SET dvr_id = (SELECT dvr_id FROM dvrs WHERE dvr_nome = %s) WHERE camera_id = %s"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (new_dvr, camera_id))
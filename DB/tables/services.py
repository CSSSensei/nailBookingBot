from typing import List

from DB.models import ServiceModel
from DB.tables.base import BaseTable


class ServicesTable(BaseTable):
    __tablename__ = 'services'

    def create_table(self):
        """Создание таблицы services"""
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            duration INTEGER,
            price REAL NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1  -- В SQLite BOOLEAN как INTEGER (0/1)
        )''')
        self.conn.commit()
        self._log('CREATE_TABLE')

    def add_service(self, service: ServiceModel) -> int:
        """Добавляет новую услугу и возвращает её ID."""
        query = f"""
        INSERT INTO {self.__tablename__} (name, description, duration, price)
        VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (service.name, service.description, service.duration, int(service.price)))
        self._log('ADD_SERVICE', name=service.name, price=service.price)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_active_services(self) -> List[ServiceModel]:
        """Возвращает список активных услуг."""
        query = f"SELECT * FROM {self.__tablename__} WHERE is_active = TRUE"
        self.cursor.execute(query)
        return [ServiceModel(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            duration=row['duration'],
            price=row['price'],
            is_active=bool(row['is_active'])
        ) for row in self.cursor]

    def toggle_service_active(self, service_id: int, is_active: bool) -> None:
        """Активирует/деактивирует услугу."""
        if not self._check_record_exists('services', 'id', service_id):
            raise ValueError(f"Service with id {service_id} not found")
        query = f"UPDATE {self.__tablename__} SET is_active = ? WHERE id = ?"
        self.cursor.execute(query, (int(is_active), service_id))
        self.conn.commit()
        self._log('TOGGLE_SERVICE_ACTIVE', service_id=service_id, is_active=is_active)

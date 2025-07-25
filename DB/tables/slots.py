from datetime import datetime, timedelta
from typing import Optional, List

from DB.models import SlotModel
from DB.tables.base import BaseTable


class SlotsTable(BaseTable):
    __tablename__ = 'slots'

    def create_table(self):
        """Создание таблицы slots"""
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.__tablename__} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            is_available BOOLEAN NOT NULL DEFAULT 1,
            UNIQUE (start_time)
        )''')
        self.conn.commit()
        self._log('CREATE_TABLE')

    def add_slot(self, start_time: datetime, end_time: datetime) -> int:
        """Добавляет новый слот для записи и возвращает его ID."""
        query = f"""
        INSERT INTO {self.__tablename__} (start_time, end_time)
        VALUES (?, ?)
        """
        self.cursor.execute(query, (start_time, end_time))
        self._log('ADD_SLOT', start_time=start_time, end_time=end_time)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_available_slots(self, from_time: Optional[datetime] = None) -> List[SlotModel]:
        """Возвращает список доступных слотов."""
        query = f"SELECT * FROM {self.__tablename__} WHERE is_available = TRUE"
        params = ()

        if from_time:
            query += " AND start_time >= ?"
            params = (from_time,)

        self.cursor.execute(query, params)
        return [SlotModel(
            id=row['id'],
            start_time=datetime.fromisoformat(row['start_time']) if row['start_time'] else None,
            end_time=datetime.fromisoformat(row['end_time']) if row['end_time'] else None,
            is_available=row['is_available']
        ) for row in self.cursor]

    def reserve_slot(self, slot_id: int) -> None:
        """Помечает слот как занятый."""
        if not self._check_record_exists('slots', 'id', slot_id):
            raise ValueError(f"Slot with id {slot_id} not found")
        query = f"UPDATE {self.__tablename__} SET is_available = FALSE WHERE id = ?"
        self.cursor.execute(query, (slot_id,))
        self.conn.commit()
        self._log('RESERVE_SLOT', slot_id=slot_id)
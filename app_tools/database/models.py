from sqlalchemy import DateTime, func, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db


class Country(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    cities: Mapped[list["City"]] = relationship(
        "City", back_populates="country"
    )


class City(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    count: Mapped[int] = mapped_column(Integer, default=0)
    country_id = mapped_column(ForeignKey("country.id"), nullable=False)
    country: Mapped[Country] = relationship("Country", back_populates="cities")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country.name,
            "count": self.count,
        }


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_session: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )


class UsersCities(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship("User")

    city_id = mapped_column(ForeignKey("city.id"))
    city: Mapped[City] = relationship("City")

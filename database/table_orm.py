from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class URLTable(Base):
    __tablename__ = "url_table"
    url_id = Column(Integer, primary_key=True, autoincrement=True)
    url_website = Column(String, nullable=False)
    extra_urls = relationship("ExtraURLTable", back_populates="url")

    def __repr__(self) -> str:
        return f"<UrlTable(url_id=%s, url_website=%s)>" % (self.url_id, self.url_website)   

class ExtraURLTable(Base):
    __tablename__ = "extra_url_table"
    url_id = Column(Integer, ForeignKey("url_table.url_id"), nullable=False)
    extra_url_link = Column(String, primary_key=True)
    url = relationship("URLTable", back_populates="extra_urls")
    stress = relationship("StressTable", uselist=False, back_populates="extra_url")
    performance = relationship("PerformanceLighthouseTable", uselist=False, back_populates="extra_url")
    responsive = relationship("ResponsiveTable", uselist=False, back_populates="extra_url")
    test_break = relationship("TestBreakTable", uselist=False, back_populates="extra_url")

    def __repr__(self) -> str:
        return f"<ExtraURLTable(extra_url_link=%s, url_id=%s)>" % (self.extra_url_link, self.url_id)

class StressTable(Base):
    __tablename__ = "stress_table"
    extra_url_link = Column(String, ForeignKey("extra_url_table.extra_url_link"), primary_key=True)
    stress_check = Column(Boolean, default=False)
    extra_url = relationship("ExtraURLTable", back_populates="stress")

    def __repr__(self) -> str:
        return f"<StressTable(extra_url_link=%s, stress_check=%s)>" % (self.extra_url_link, self.stress_check)

class PerformanceLighthouseTable(Base):
    __tablename__ = "performance_lighthouse_table"
    extra_url_link = Column(String, ForeignKey("extra_url_table.extra_url_link"), primary_key=True)
    performance_lighthouse = Column(Boolean, default=False)
    extra_url = relationship("ExtraURLTable", back_populates="performance")

    def __repr__(self) -> str:
        return f"<PerformanceLighthouseTable(extra_url_link=%s, performance_lighthouse=%s)>" % (self.extra_url_link, self.performance_lighthouse)

class ResponsiveTable(Base):
    __tablename__ = "responsive_table"
    extra_url_link = Column(String, ForeignKey("extra_url_table.extra_url_link"), primary_key=True)
    tablet = Column(Boolean, default=False)
    fold_phone = Column(Boolean, default=False)
    normal_phone = Column(Boolean, default=False)
    desktop = Column(Boolean, default=False)
    extra_url = relationship("ExtraURLTable", back_populates="responsive")

    def __repr__(self) -> str:
        return f"<ResponsiveTable(extra_url_link=%s, tablet=%s, fold_phone=%s, normal_phone=%s, desktop=%s)>" % (self.extra_url_link, self.tablet, self.fold_phone, self.normal_phone, self.desktop)

class TestBreakTable(Base):
    __tablename__ = "test_break_table"
    extra_url_link = Column(String, ForeignKey("extra_url_table.extra_url_link"), primary_key=True)
    test_to_break = Column(Boolean, default=False)
    extra_url = relationship("ExtraURLTable", back_populates="test_break")

    def __repr__(self) -> str:
        return f"<TestBreakTable(extra_url_link=%s, test_to_break=%s)>" % (self.extra_url_link, self.test_to_break)


DATABASE_URL = "postgresql://zed:zed@localhost:5432/url"
engine = create_engine(DATABASE_URL)
# engine = create_engine("sqlite:///:memory:")
# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)



if __name__ == "__main__":

    # Create tables
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)

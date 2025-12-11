from sqlalchemy import Column,Integer,String ,DateTime,ForeignKey,Text,func 
from sqlalchemy.orm import relationship
from api_app.database import Base


# Table des logs d'analyses
class AnalysisLog(Base):
    __tablename__ = "analysis_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    input_text = Column(Text, nullable=False)
    analysis_result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # L’utilisateur qui a créé ce log
    user = relationship("USER", back_populates="logs")

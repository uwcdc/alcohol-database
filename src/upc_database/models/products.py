from sqlmodel import SQLModel, Field, Float, String, DateTime, Text, UUID
from pydantic import field_validator
from typing import Optional
from datetime import datetime
import uuid

@classmethod
def validate_upc(cls, v, field):
    # Validate UPC-A and UPC-E str; UPC-A must be 12 digits and UPC-E must be 8 digits
    if field.name == 'upc_a' or field.name == 'carton_upc' or field.name == 'case_upc':
        if v is not None and (len(v) != 12 or not v.isdigit()):
            raise ValueError(f"Invalid UPC-A: {v}. It must be a 12-digit numeric string.")
    elif field.name == 'upc_e':
        if v is not None and (len(v) != 8 or not v.isdigit()):
            raise ValueError(f"Invalid UPC-E: {v}. It must be an 8-digit numeric string.")
    return v

@classmethod
def validate_bv(cls, v):
    if v is not None and (v <= 0 or v > 100):
        raise ValueError(f"Invalid ABV: {v}. It must be between 0 and 100.")
    return v

class Products(SQLModel, table=True):
    __tablename__ = "products"
    __tableargs__ = {"schema": "public"}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str = Field(index=True, max_length=255, sa_type=String(255))  # Name of the product
    db_category_id: Optional[int] = Field(default=None, foreign_key="db_category.id")  # Foreign key to original database table
    product_category_id: Optional[int] = Field(default=None, foreign_key="product_category.id")  # Foreign key
    product_sub_category_id: Optional[int] = Field(default=None, foreign_key="product_sub_category.id")  # Foreign key
    spirit_styles_id: Optional[int] = Field(default=None, foreign_key="spirit_styles.id")  # Foreign key
    nacs_categories_id: Optional[int] = Field(default=None, foreign_key="nacs_categories.id")  # Foreign key
    upc_e: Optional[str] = Field(default=None, index=True, max_length=8, sa_type=String(8))  # GTIN-8 for UPC/EAN; Pass as string
    upc_a: Optional[str] = Field(default=None, index=True, max_length=12, sa_type=String(12))  # GTIN-12 for UPC-A; Pass as string
    product_description: Optional[str] = Field(default=None, sa_type=Text) # Description of the product
    description_note: Optional[str] = Field(default=None, sa_type=Text) # Additional description notes
    count: Optional[float] = Field(default=1, sa_type=Float) # Count (e.g., number of items per pack)
    carton_upc: Optional[str] = Field(default=None, sa_type=String) # Carton UPC
    case_upc: Optional[str] = Field(default=None, sa_type=String) # Case UPC
    countries_id: Optional[int] = Field(default=None, foreign_key="countries.id")  # Foreign key to countries table
    states_id: Optional[int] = Field(default=None, foreign_key="states.id")  # Foreign key to states table
    regions_id: Optional[int] = Field(default=None, foreign_key="regions.id")  # Foreign key to regions table
    varietals_id: Optional[int] = Field(default=None, foreign_key="varietals.id")  # Foreign key to varietals table
    appellations_id: Optional[int] = Field(default=None, foreign_key="appellations.id")  # Foreign key to appellations table
    vintage_key_id: Optional[int] = Field(default=None, foreign_key="vintage_key.id")  # Foreign key to vintage_key table
    databases_id: Optional[int] = Field(default=None, foreign_key="databases.id")  # Foreign key to databases table
    manufacturers_id: Optional[int] = Field(default=None, foreign_key="manufacturers.id")  # Foreign key to manufacturers table
    brand_lines_id: Optional[int] = Field(default=None, foreign_key="brand_lines.id")  # Foreign key to brand_lines table
    model_mpn_ndc: Optional[str] = Field(default=None, sa_type=String) # Model/Manufacturer Part Number/National Drug Code
    containers_id: Optional[int] = Field(default=None, foreign_key="containers.id")  # Foreign key to containers table
    warnings: Optional[str] = Field(default=None, sa_type=Text) # Product warnings
    abv: Optional[float] = Field(default=None, sa_type=Float) # Alcohol by Volume (ABV)
    ibu: Optional[float] = Field(default=None, sa_type=Float) # International Bitterness Units (IBU)
    prepared_notes_and_health_claims: Optional[str] =  Field(default=None, sa_type=Text) # Prepared notes and health claims
    created_at: Optional[datetime] = Field(default_factory=datetime.now, index=True, nullable=False, sa_type=DateTime)  # Timestamp when the product was created
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, index=True, sa_type=DateTime)  # Timestamp when the product was updated
    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="auth.users.id", sa_type=UUID)  # User who created the product
    updated_by: Optional[uuid.UUID] = Field(default=None, foreign_key="auth.users.id", sa_type=UUID)  # User who last updated the product
    
    _upc = field_validator('upc_a', 'upc_e', 'carton_upc', 'case_upc', pre=True, always=True)(validate_upc)
    
    _by_volume = field_validator('abv', 'ibv', pre=True, always=True)(validate_bv)

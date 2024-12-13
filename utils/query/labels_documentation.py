from uuid import uuid4
from services.postgres.connection import database_connection
from utils.custom_errors import DatabaseQueryError, DataNotFoundError
from sqlmodel.main import SQLModelMetaclass
from utils.logger import logging
from utils.helper import local_time
from sqlalchemy import insert, select
from services.postgres.models import (
    CategoryDataDocumentation,
    ObjectDocumentationDetails,
    EnvironmentDocumentationDetails,
    DesignTypeDocumentationDetails,
    TimePeriodDocumentationDetails,
    DominantColorDocumentationDetails,
    CultureStyleDocumentationDetails
)


async def validate_data_availability(table_model: SQLModelMetaclass) -> bool:
    """
    This Python async function validates the availability of data in a database table using an
    SQLModelMetaclass object.

    :param table_model: The `table_model` parameter in the `validate_data_availability` function is
    expected to be a SQLAlchemy model class that represents a table in the database. This class should
    be a subclass of `SQLModelMetaclass`, which is likely a custom metaclass for SQLAlchemy models in
    your codebase. The
    :type table_model: SQLModelMetaclass
    :return: The function `validate_data_availability` returns a boolean value indicating whether the
    data represented by the `table_model` exists in the database. If the data exists, it returns `True`,
    otherwise it returns `False`.
    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = select(select(table_model).exists())
            result = await session.execute(query)
            return result.scalar()

        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[validate_data_availability] Error while validating data availability: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query")
        finally:
            await session.close()

    return False


async def insert_category_documentation(
    table_model: SQLModelMetaclass, category: str, description: str
) -> str:
    """
    This async function inserts documentation for a category into a database table and returns the
    unique ID generated for the entry.

    :param table_model: The `table_model` parameter in the `insert_category_documentation` function is
    expected to be a SQLModelMetaclass object. This object likely represents a table in a database and
    is used to define the structure and properties of the table
    :type table_model: SQLModelMetaclass
    :param category: The `category` parameter in the `insert_category_documentation` function represents
    the category of the document being inserted into the database. It is a string that describes the
    category to which the document belongs. For example, if you are inserting a document related to
    "Technology", then "Technology" would be
    :type category: str
    :param description: The `insert_category_documentation` function is an asynchronous function that
    inserts a new category document into a database table using the provided `table_model`, `category`,
    and `description` parameters
    :type description: str
    :return: The function `insert_category_documentation` is returning the unique identifier
    (`unique_id`) of the inserted category documentation.
    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            unique_id = str(uuid4())
            query = insert(table_model).values(
                created_at=local_time(),
                unique_id=unique_id,
                category=category,
                description=description,
            )
            await session.execute(query)
            await session.commit()
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[validate_data_availability] Error while validating data availability: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query")
        finally:
            await session.close()

    return unique_id


async def insert_details_documentation(
    table_model: SQLModelMetaclass, unique_id: str, category: str, description: str
) -> None:
    """
    This asynchronous function inserts details documentation into a database table using the provided
    parameters.

    :param table_model: The `table_model` parameter in the `insert_details_documentation` function is
    expected to be a SQLModelMetaclass object. This object likely represents a table in a database and
    is used to define the structure and properties of the table
    :type table_model: SQLModelMetaclass
    :param unique_id: The `unique_id` parameter in the `insert_details_documentation` function is a
    string that represents a unique identifier for the document being inserted into the database. It is
    used as a key to uniquely identify the document within the database table
    :type unique_id: str
    :param category: The `category` parameter in the `insert_details_documentation` function represents
    the category to which the details being inserted belong. It is a string that helps classify or
    categorize the information being stored in the database. For example, if you are inserting details
    about products, the category could be "electronics
    :type category: str
    :param description: The `insert_details_documentation` function is an asynchronous function that
    inserts details into a database table. The function takes the following parameters:
    :type description: str
    :return: The function `insert_details_documentation` is returning `None`.
    """
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = insert(table_model).values(
                created_at=local_time(),
                unique_id=unique_id,
                category=category,
                description=description,
            )
            await session.execute(query)
            await session.commit()
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[validate_data_availability] Error while validating data availability: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query")
        finally:
            await session.close()

    return None


async def insert_object_documentation() -> None:
    logging.info("Insert object details entry.")
    unique_id = await insert_category_documentation(
        table_model=CategoryDataDocumentation,
        category="object",
        description="Represents physical items or elements that are the main focus of an image.",
    )
    await insert_details_documentation(
        table_model=ObjectDocumentationDetails,
        unique_id=unique_id,
        category="artifacts",
        description="Man-made items that are often decorative or artistic. (e.g: statues, window, glass, pillars, curtain, fountains, particles, etc.)",
    )
    await insert_details_documentation(
        table_model=ObjectDocumentationDetails,
        unique_id=unique_id,
        category="nature",
        description="Natural elements commonly found in outdoor settings. (e.g: mountains, flowers, trees, root, etc.)",
    )
    await insert_details_documentation(
        table_model=ObjectDocumentationDetails,
        unique_id=unique_id,
        category="living_beings",
        description="Refers to animals or other living creatures present in the image. (e.g: human, couple, and butterfly, etc.)",
    )
    return None


async def insert_environment_documentation() -> None:
    logging.info("Insert environment details entry.")
    unique_id = await insert_category_documentation(
        table_model=CategoryDataDocumentation,
        category="environment",
        description="Describes the surrounding setting or background context where the image takes place.",
    )
    await insert_details_documentation(
        table_model=EnvironmentDocumentationDetails,
        unique_id=unique_id,
        category="natural",
        description="Outdoor and organic settings. (e.g: gardens, forests, waterfalls, oceans, underwater, flower-ish, etc.)",
    )
    await insert_details_documentation(
        table_model=EnvironmentDocumentationDetails,
        unique_id=unique_id,
        category="manmade",
        description="Human-created settings. (e.g: ballrooms, libraries, rustic, glasshouses, etc.)",
    )
    await insert_details_documentation(
        table_model=EnvironmentDocumentationDetails,
        unique_id=unique_id,
        category="conceptual",
        description="Imaginative or themed environments. (e.g: galaxy, disney, abstract, gatsby, etc.).",
    )
    return None

async def insert_design_type_documentation() -> None:
    logging.info("Insert design_type details entry.")
    unique_id = await insert_category_documentation(
        table_model=CategoryDataDocumentation,
        category="design_type",
        description="Refers to the artistic or architectural style depicted in the image, often conveying the overall 'feel' or aesthetic of the scene.",
    )
    await insert_details_documentation(
        table_model=DesignTypeDocumentationDetails,
        unique_id=unique_id,
        category="art_deco",
        description="A decorative style characterized by rich and luxury colors. (e.g: awarding image, bold geometry, etc.)",
    )
    await insert_details_documentation(
        table_model=DesignTypeDocumentationDetails,
        unique_id=unique_id,
        category="heaven",
        description="A conceptual style depicting divine or ethereal imagery. (e.g: rich of light image, heavenly feel image, etc.)",
    )
    await insert_details_documentation(
        table_model=DesignTypeDocumentationDetails,
        unique_id=unique_id,
        category="architectural",
        description="Design elements focusing on buildings or structures. (e.g: churches, chinese house, etc.).",
    )
    await insert_details_documentation(
        table_model=DesignTypeDocumentationDetails,
        unique_id=unique_id,
        category="artistic",
        description="Images that emphasize creativity, painting, or artistic interpretation. (e.g: painting image.)",
    )
    await insert_details_documentation(
        table_model=DesignTypeDocumentationDetails,
        unique_id=unique_id,
        category="sci_fi",
        description="A futuristic style involving science fiction elements. (e.g: planet-ish image.)",
    )
    await insert_details_documentation(
        table_model=DesignTypeDocumentationDetails,
        unique_id=unique_id,
        category="fantasy",
        description="A style rooted in mythical or magical themes. (e.g: high fog image, scary halloween-ish image, etc.)",
    )
    return None

async def insert_time_period_documentation() -> None:
    logging.info("Insert time_period details entry.")
    unique_id = await insert_category_documentation(
        table_model=CategoryDataDocumentation,
        category="time_period",
        description="Specifies the context of time in the image.",
    )
    await insert_details_documentation(
        table_model=TimePeriodDocumentationDetails,
        unique_id=unique_id,
        category="day",
        description="Scenes illuminated by daylight.",
    )
    await insert_details_documentation(
        table_model=TimePeriodDocumentationDetails,
        unique_id=unique_id,
        category="afternoon",
        description="Images depicting the time after noon, with softer lighting.",
    )
    await insert_details_documentation(
        table_model=TimePeriodDocumentationDetails,
        unique_id=unique_id,
        category="evening",
        description="Scenes capturing the time before sunset or early night.",
    )
    await insert_details_documentation(
        table_model=TimePeriodDocumentationDetails,
        unique_id=unique_id,
        category="night",
        description="Images set in the dark or natural low light.",
    )
    
    return None

async def insert_dominant_colors_documentation() -> None:
    logging.info("Insert dominant_colors details entry.")
    unique_id = await insert_category_documentation(
        table_model=CategoryDataDocumentation,
        category="dominant_colors",
        description="Showcases the main color scheme or palette that stands out in the image.",
    )
    await insert_details_documentation(
        table_model=DominantColorDocumentationDetails,
        unique_id=unique_id,
        category="warm",
        description="Colors that evoke warmth and energy. (e.g: red, yellow, pink, etc.)",
    )
    await insert_details_documentation(
        table_model=DominantColorDocumentationDetails,
        unique_id=unique_id,
        category="cool",
        description="Colors that convey calmness and serenity. (e.g: blue, green, purple, etc.)",
    )
    await insert_details_documentation(
        table_model=DominantColorDocumentationDetails,
        unique_id=unique_id,
        category="neutral",
        description="Basic colors which are versatile and understated. (e.g: white, gray, and black, etc.)",
    )
    await insert_details_documentation(
        table_model=DominantColorDocumentationDetails,
        unique_id=unique_id,
        category="gold",
        description="A metallic color often associated with luxury and richness. (e.g: gold.)",
    )
    
    return None

async def insert_culture_styles_documentation() -> None:
    logging.info("Insert culture_styles details entry.")
    unique_id = await insert_category_documentation(
        table_model=CategoryDataDocumentation,
        category="culture_styles",
        description="Highlights the cultural or regional influences evident in the image's style and elements.",
    )
    await insert_details_documentation(
        table_model=CultureStyleDocumentationDetails,
        unique_id=unique_id,
        category="asian",
        description="Styles inspired by Asian countries cultures. (e.g: Indonesia, Singapore, Arab, India, Korea, Japan, Chinese, etc.)",
    )
    await insert_details_documentation(
        table_model=CultureStyleDocumentationDetails,
        unique_id=unique_id,
        category="european",
        description="Aesthetic styles from European countries, often classical or modern. (e.g: Rome, Italy, etc.)",
    )
    
    
    return None

async def initialize_labels_documentation() -> None:
    is_available = await validate_data_availability(table_model=CategoryDataDocumentation)
    if not is_available:
        logging.info("Initialized labels documentation.")
        await insert_object_documentation()
        await insert_environment_documentation()
        await insert_design_type_documentation()
        await insert_time_period_documentation()
        await insert_dominant_colors_documentation()
        await insert_culture_styles_documentation()
    return None

async def retrieve_all(table_model: SQLModelMetaclass) -> list:
    '''This function retrieves all entries from a database table using an asynchronous connection and
    returns them as a list of dictionaries.
    
    Parameters
    ----------
    table_model : SQLModelMetaclass
        The `table_model` parameter in the `retrieve_all` function is expected to be a class that
    represents a table in a SQL database. It is likely a SQLAlchemy model class that is defined using
    the `SQLModelMetaclass`. This class would typically have attributes that define the structure of the
    table,
    
    Returns
    -------
        The function `retrieve_all` is returning a list of dictionaries where each dictionary represents a
    row of data retrieved from the database table specified by the `table_model` parameter. Each
    dictionary contains key-value pairs where the keys are the column names of the table and the values
    are the corresponding data values for that row.
    
    '''
    async with database_connection(connection_type="async").connect() as session:
        try:
            query = select(table_model)
            result = await session.execute(query)
            rows = result.fetchall()

            if not rows:
                logging.error(f"[retrieve_all] No data entry in {table_model.__tablename__}!")
                raise DataNotFoundError("Data entry not found.")
            
            result = [dict(row._mapping) for row in rows]

        except DataNotFoundError:
            raise
        except DatabaseQueryError:
            raise
        except Exception as e:
            logging.error(
                f"[retrieve_all] Error retieving all entry: {e}"
            )
            await session.rollback()
            raise DatabaseQueryError(detail="Invalid database query")
        finally:
            await session.close()

    return result


async def retrieve_labels_documentation() -> dict:
    wrapper = {}
    
    general = await retrieve_all(table_model=CategoryDataDocumentation)
    object = await retrieve_all(table_model=ObjectDocumentationDetails)
    environment = await retrieve_all(table_model=EnvironmentDocumentationDetails)
    design_type = await retrieve_all(table_model=DesignTypeDocumentationDetails)
    time_period = await retrieve_all(table_model=TimePeriodDocumentationDetails)
    dominant_color = await retrieve_all(table_model=DominantColorDocumentationDetails)
    culture_style = await retrieve_all(table_model=CultureStyleDocumentationDetails)

    for category in general:
        if category["category"] == "object":
            category["details"] = object
        if category["category"] == "environment":
            category["details"] = environment
        if category["category"] == "design_type":
            category["details"] = design_type
        if category["category"] == "time_period":
            category["details"] = time_period
        if category["category"] == "dominant_colors":
            category["details"] = dominant_color
        if category["category"] == "culture_styles":
            category["details"] = culture_style
    
    wrapper["documentation"] = general
    return wrapper
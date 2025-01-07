from utils.logger import logging
from uuid import uuid4
from utils.custom_errors import DatabaseQueryError, ServiceError, DiVA
from services.postgres.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from utils.query.general import find_record, insert_record
from services.postgres.models import (
    CategoryDataDocumentation,
    ObjectDocumentationDetails,
    EnvironmentDocumentationDetails,
    DesignTypeDocumentationDetails,
    TimePeriodDocumentationDetails,
    DominantColorDocumentationDetails,
    CultureStyleDocumentationDetails,
)


async def insert_object_documentation(db: AsyncSession) -> None:
    unique_id = str(uuid4())

    try:
        logging.info("Insert object detail entries.")
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={
                "unique_id": unique_id,
                "category": "object",
                "description": "Represents physical items or elements that are the main focus of an image.",
            },
        )
        await insert_record(
            db=db,
            table=ObjectDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "artifacts",
                "description": "Man-made items that are often decorative or artistic. (e.g: statues, window, glass, pillars, curtain, fountains, particles, etc.)",
            },
        )
        await insert_record(
            db=db,
            table=ObjectDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "nature",
                "description": "Natural elements commonly found in outdoor settings. (e.g: mountains, flowers, trees, root, etc.)",
            },
        )
        await insert_record(
            db=db,
            table=ObjectDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "living_beings",
                "description": "Refers to animals or other living creatures present in the image. (e.g: human, couple, and butterfly, etc.)",
            },
        )

    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        logging.error(f"Error while inserting object documentation: {e}")
        raise ServiceError(detail="Database query error.")
    return None


async def insert_environment_documentation(db: AsyncSession) -> None:
    unique_id = str(uuid4())
    try:
        pass
        logging.info("Insert environment detail entries.")
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={
                "unique_id": unique_id,
                "category": "environment",
                "description": "Describes the surrounding setting or background context where the image takes place.",
            },
        )

        await insert_record(
            db=db,
            table=EnvironmentDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "natural",
                "description": "Outdoor and organic settings. (e.g: gardens, forests, waterfalls, oceans, underwater, flower-ish, etc.)",
            },
        )

        await insert_record(
            db=db,
            table=EnvironmentDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "manmade",
                "description": "Human-created settings. (e.g: ballrooms, libraries, rustic, glasshouses, etc.)",
            },
        )

        await insert_record(
            db=db,
            table=EnvironmentDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "conceptual",
                "description": "Imaginative or themed environments. (e.g: galaxy, disney, abstract, gatsby, etc.)",
            },
        )

    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        logging.error(f"Error while inserting environment documentation: {e}")
        raise ServiceError(detail="Database query error.")
    return None


async def insert_design_type_documentation(db: AsyncSession) -> None:
    unique_id = str(uuid4())
    try:
        logging.info("Insert design_type entries.")
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={
                "unique_id": unique_id,
                "category": "design_type",
                "description": "Refers to the artistic or architectural style depicted in the image, often conveying the overall 'feel' or aesthetic of the scene.",
            },
        )

        await insert_record(
            db=db,
            table=DesignTypeDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "art_deco",
                "description": "A decorative style characterized by rich and luxury colors. (e.g: awarding image, bold geometry, etc.)",
            },
        )

        await insert_record(
            db=db,
            table=DesignTypeDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "heaven",
                "description": "A conceptual style depicting divine or ethereal imagery. (e.g: rich of light image, heavenly feel image, etc.)",
            },
        )

        await insert_record(
            db=db,
            table=DesignTypeDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "architectural",
                "description": "Design elements focusing on buildings or structures. (e.g: churches, chinese house, etc.).",
            },
        )

        await insert_record(
            db=db,
            table=DesignTypeDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "artistic",
                "description": "Images that emphasize creativity, painting, or artistic interpretation. (e.g: painting image.)",
            },
        )

        await insert_record(
            db=db,
            table=DesignTypeDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "sci_fi",
                "description": "A futuristic style involving science fiction elements. (e.g: planet-ish image.)",
            },
        )

        await insert_record(
            db=db,
            table=DesignTypeDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "fantasy",
                "description": "A style rooted in mythical or magical themes. (e.g: high fog image, scary halloween-ish image, etc.)",
            },
        )
    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        logging.error(f"Error while inserting environment documentation: {e}")
        raise ServiceError(detail="Database query error.")
    return None


async def insert_time_period_documentation(db: AsyncSession) -> None:
    unique_id = str(uuid4())
    try:
        logging.info("Insert time_period entries.")
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={
                "unique_id": unique_id,
                "category": "time_period",
                "description": "Specifies the context of time in the image.",
            },
        )

        await insert_record(
            db=db,
            table=TimePeriodDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "day",
                "description": "Scenes illuminated by daylight.",
            },
        )

        await insert_record(
            db=db,
            table=TimePeriodDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "afternoon",
                "description": "Images depicting the time after noon, with softer lighting.",
            },
        )

        await insert_record(
            db=db,
            table=TimePeriodDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "evening",
                "description": "Scenes capturing the time before sunset or early night.",
            },
        )

        await insert_record(
            db=db,
            table=TimePeriodDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "night",
                "description": "Images set in the dark or natural low light.",
            },
        )

    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        logging.error(f"Error while inserting environment documentation: {e}")
        raise ServiceError(detail="Database query error.")
    return None


async def insert_dominant_colors_documentation(db: AsyncSession) -> None:
    unique_id = str(uuid4())
    try:
        logging.info("Insert dominant_color entries.")
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={
                "unique_id": unique_id,
                "category": "dominant_colors",
                "description": "Showcases the main color scheme or palette that stands out in the image.",
            },
        )

        await insert_record(
            db=db,
            table=DominantColorDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "warm",
                "description": "Colors that evoke warmth and energy. (e.g: red, yellow, pink, etc.)",
            },
        )

        await insert_record(
            db=db,
            table=DominantColorDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "cool",
                "description": "Colors that convey calmness and serenity. (e.g: blue, green, purple, etc.)",
            },
        )

        await insert_record(
            db=db,
            table=DominantColorDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "neutral",
                "description": "Basic colors which are versatile and understated. (e.g: white, gray, and black, etc.)",
            },
        )

        await insert_record(
            db=db,
            table=DominantColorDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "gold",
                "description": "A metallic color often associated with luxury and richness. (e.g: gold.)",
            },
        )
    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        logging.error(f"Error while inserting environment documentation: {e}")
        raise ServiceError(detail="Database query error.")
    return None


async def insert_culture_styles_documentation(db: AsyncSession):
    unique_id = str(uuid4())

    try:
        logging.info("Insert culture_style entries.")
        await insert_record(
            db=db,
            table=CategoryDataDocumentation,
            data={
                "unique_id": unique_id,
                "category": "culture_styles",
                "description": "Highlights the cultural or regional influences evident in the image's style and elements.",
            },
        )

        await insert_record(
            db=db,
            table=CultureStyleDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "asian",
                "description": "Styles inspired by Asian countries cultures. (e.g: Indonesia, Singapore, Arab, India, Korea, Japan, Chinese, etc.)",
            },
        )

        await insert_record(
            db=db,
            table=CultureStyleDocumentationDetails,
            data={
                "unique_id": unique_id,
                "category": "european",
                "description": "Aesthetic styles from European countries, often classical or modern. (e.g: Rome, Italy, etc.)",
            },
        )

    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        logging.error(f"Error while inserting environment documentation: {e}")
        raise ServiceError(detail="Database query error.")
    return None


async def initialize_labels_documentation() -> None:
    try:
        async for db in get_db():
            category_record = await find_record(db=db, table=CategoryDataDocumentation)
            if not category_record:
                logging.info("Initialized labels documentation.")
                await insert_object_documentation(db=db)
                await insert_environment_documentation(db=db)
                await insert_design_type_documentation(db=db)
                await insert_time_period_documentation(db=db)
                await insert_dominant_colors_documentation(db=db)
                await insert_culture_styles_documentation(db=db)
            break
        logging.info("Labels documentation already initialized.")
    except DiVA:
        raise
    except DatabaseQueryError:
        raise
    except Exception as e:
        logging.error(f"Error while inserting environment documentation: {e}")
        raise ServiceError(detail="Database query error.")
    return None

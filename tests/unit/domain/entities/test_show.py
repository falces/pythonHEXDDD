"""
Tests unitarios para la entidad Show.
"""

import pytest
from Domain.Show.Show import Show
from Domain.Show.ValueObjects.ShowId import ShowId
from Domain.Show.ValueObjects.ShowTitle import ShowTitle
from Domain.Show.ValueObjects.ShowType import ShowType
from Domain.Show.ValueObjects.StreamingOption import StreamingOption


class TestShow:
    """Tests para la entidad Show."""
    
    def test_create_show_with_all_attributes(self):
        """Debería crear un Show con todos los atributos."""
        # Arrange
        show_id = ShowId("tt1234567")
        title = ShowTitle("Breaking Bad")
        show_type = ShowType("series")
        streaming_options = [
            StreamingOption("Netflix", "subscription"),
            StreamingOption("Amazon", "subscription")
        ]
        
        # Act
        show = Show(
            show_id=show_id,
            title=title,
            show_type=show_type,
            streaming_options=streaming_options
        )
        
        # Assert
        assert show.show_id.value == "tt1234567"
        assert show.title.value == "Breaking Bad"
        assert show.show_type.is_series()
        assert len(show.streaming_options) == 2
    
    def test_show_is_movie_returns_true_for_movie(self):
        """isMovie() debería retornar True para películas."""
        # Arrange
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("The Matrix"),
            show_type=ShowType("movie"),
            streaming_options=[]
        )
        
        # Act & Assert
        assert show.isMovie() is True
        assert show.isSeries() is False
    
    def test_show_is_series_returns_true_for_series(self):
        """isSeries() debería retornar True para series."""
        # Arrange
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("Breaking Bad"),
            show_type=ShowType("series"),
            streaming_options=[]
        )
        
        # Act & Assert
        assert show.isSeries() is True
        assert show.isMovie() is False
    
    def test_show_has_streaming_option_returns_true_when_present(self):
        """hasStreamingOption() debería retornar True si existe la opción."""
        # Arrange
        streaming_options = [
            StreamingOption("Netflix", "subscription"),
            StreamingOption("Amazon", "subscription")
        ]
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("Test Show"),
            show_type=ShowType("movie"),
            streaming_options=streaming_options
        )
        
        # Act & Assert
        assert show.hasStreamingOption("Netflix") is True
        assert show.hasStreamingOption("HBO") is False
    
    def test_show_with_no_streaming_options(self):
        """Debería poder crear un Show sin opciones de streaming."""
        # Arrange & Act
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("Test Show"),
            show_type=ShowType("movie"),
            streaming_options=[]
        )
        
        # Assert
        assert len(show.streaming_options) == 0
        assert show.hasStreamingOption("Netflix") is False
    
    def test_show_with_multiple_streaming_options(self):
        """Debería manejar múltiples opciones de streaming."""
        # Arrange
        streaming_options = [
            StreamingOption("Netflix", "subscription"),
            StreamingOption("Amazon Prime", "subscription"),
            StreamingOption("Apple TV", "buy"),
            StreamingOption("Google Play", "rent")
        ]
        
        # Act
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("Popular Movie"),
            show_type=ShowType("movie"),
            streaming_options=streaming_options
        )
        
        # Assert
        assert len(show.streaming_options) == 4
        assert show.hasStreamingOption("Netflix") is True
        assert show.hasStreamingOption("Apple TV") is True

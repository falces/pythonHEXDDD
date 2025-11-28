"""
Tests unitarios para la entidad Show.
"""

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
        streaming_option = StreamingOption("Netflix", "subscription")

        # Act
        show = Show(
            show_id=show_id,
            title=title,
            show_type=show_type,
            streaming_option=streaming_option
        )

        # Assert
        assert show.show_id.value == "tt1234567"
        assert show.title.value == "Breaking Bad"
        assert show.show_type.is_series()
        assert show.streaming_option is not None

    def test_show_is_movie_returns_true_for_movie(self):
        """is_movie() debería retornar True para películas."""
        # Arrange
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("The Matrix"),
            show_type=ShowType("movie"),
            streaming_option=None
        )

        # Act & Assert
        assert show.is_movie() is True
        assert show.is_series() is False

    def test_show_is_series_returns_true_for_series(self):
        """is_series() debería retornar True para series."""
        # Arrange
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("Breaking Bad"),
            show_type=ShowType("series"),
            streaming_option=None
        )

        # Act & Assert
        assert show.is_series() is True
        assert show.is_movie() is False

    def test_show_has_streaming_option_returns_true_when_present(self):
        """has_streaming_option() debería retornar True si existe la opción."""
        # Arrange
        streaming_option = StreamingOption("Netflix", "subscription")
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("Test Show"),
            show_type=ShowType("movie"),
            streaming_option=streaming_option
        )

        # Act & Assert
        assert show.has_streaming_option() is True

    def test_show_with_no_streaming_option(self):
        """Debería poder crear un Show sin opción de streaming."""
        # Arrange & Act
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("Test Show"),
            show_type=ShowType("movie"),
            streaming_option=None
        )

        # Assert
        assert show.streaming_option is None
        assert show.has_streaming_option() is False

    def test_show_getters(self):
        """Debería retornar valores correctos con los getters."""
        # Arrange
        streaming_option = StreamingOption("Netflix", "subscription")

        # Act
        show = Show(
            show_id=ShowId("tt1234567"),
            title=ShowTitle("Popular Movie"),
            show_type=ShowType("movie"),
            streaming_option=streaming_option
        )

        # Assert
        assert show.get_id() == "tt1234567"
        assert show.get_title() == "Popular Movie"
        assert show.get_type() == "movie"
        assert show.get_streaming_option() == streaming_option

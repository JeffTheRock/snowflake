
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from .collections import SoundCollection, AssetCollection
from .asset import Asset
from .sound import Sound

if TYPE_CHECKING:
    from app.engine.penguin import Penguin
    from app.engine.game import Game

class GameObject:
    def __init__(
        self,
        game: "Game",
        name: str,
        x: int = 0,
        y: int = 0,
        assets=AssetCollection(),
        sounds=SoundCollection(),
        on_click: Callable | None = None,
        grid: bool = False
    ) -> None:
        self.game = game
        self.name = name
        self.id = -1
        self.x = x
        self.y = y
        self.assets = assets
        self.sounds = sounds
        self.game.objects.add(self)
        self.on_click = on_click
        self.grid = grid

        # Place object in grid
        if grid: self.game.grid[x, y] = self

    def __eq__(self, other: object) -> bool:
        if not getattr(other, 'id', None):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def from_asset(
        cls,
        name: str,
        game: "Game",
        x: int = 0,
        y: int = 0
    ) -> "GameObject":
        asset = Asset.from_name(name)
        return GameObject(
            game,
            name,
            x,
            y,
            AssetCollection([asset])
        )

    def place_object(self) -> None:
        x = self.x
        y = self.y

        if self.grid:
            x = self.x + self.game.grid.x_offset
            y = self.y + self.game.grid.y_offset

        self.game.send_tag(
            'O_HERE',
            self.id,
            '0:1',  # TODO
            x,
            y,
            0,      # TODO
            1,      # TODO
            0,      # TODO
            0,      # TODO
            0,      # TODO
            '',     # TODO
            '0:1',  # TODO
            0,      # TODO
            1,      # TODO
            0       # TODO
        )

    def remove_object(self) -> None:
        self.game.send_tag('O_GONE', self.id)
        self.game.objects.remove(self)
        self.game.grid.remove(self)

    def animate_object(
        self,
        name: str,
        play_style: str = 'play_once',
        duration: int | None = None,
        time_scale: int = 1,
        reset: bool = False,
        callback: Callable | None = None
    ) -> None:
        asset = self.assets.by_name(name)
        self.game.send_tag(
            'O_ANIM',
            self.id,
            f'0:{asset.index}',
            play_style,
            duration or '',
            time_scale,
            int(not reset),
            self.id, # response object id
            0        # handle id
        )

        # TODO: Implement callbacks

    def place_sprite(self, name: str, target: "Penguin" | None = None) -> None:
        asset = self.assets.by_name(name)

        if target is None:
            target = self.game

        target.send_tag(
            'O_SPRITE',
            self.id,
            f'0:{asset.index}',
            0, # TODO
            '' # TODO
        )

    def load_sprite(self, name: str) -> None:
        asset = self.assets.by_name(name)
        self.game.send_tag(
            'S_LOADSPRITE',
            f'0:{asset.index}'
        )

    def load_sprites(self) -> None:
        for asset in self.assets:
            self.game.send_tag(
                'S_LOADSPRITE',
                f'0:{asset.index}'
            )

    def animate_sprite(
        self,
        start_frame: int = 0,
        end_frame: int = 0,
        backwards: bool = False,
        play_style = 'play_once',
        duration: int = 50,
    ) -> None:
        self.game.send_tag(
            'O_SPRITEANIM',
            self.id,
            start_frame + 1,
            end_frame + 1,
            int(backwards),
            play_style,
            duration
        )

    def add_sound(
        self,
        name: str,
        looping: bool = False,
        volume: int = 100,
        radius: int = 0
    ) -> None:
        self.sounds.add(
            Sound.from_name(
                name,
                looping,
                volume,
                radius,
                self.id,
                self.id # TODO: Different id for response object?
            )
        )

    def play_sound(self, sound_name: str) -> None:
        sound = self.sounds.by_name(sound_name)
        sound.play(self.game)

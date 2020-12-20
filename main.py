import asyncio
import logging
import random
import sys

import aiohttp

from game import Game
from minimax import Minimax

logging.basicConfig(level=logging.DEBUG)


class ApiTester:
    def __init__(self, loop, player_num):
        self._api_url = 'http://localhost:8081'
        self._game = Game()
        self._session = aiohttp.ClientSession()
        self._player_num = player_num
        self._loop = loop
        self._last_move = []

    async def _prepare_player(self, num):
        async with self._session.post(
                f'{self._api_url}/game',
                params={'team_name': num}
        ) as resp:
            res = (await resp.json())['data']
            self._player = {
                'color': res['color'],
                'token': res['token']
            }

    async def _make_move(self, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._player["token"]}'}
        async with self._session.post(
                f'{self._api_url}/move',
                json=json,
                headers=headers
        ) as resp:
            print(await resp.text())
            resp = (await resp.json())['data']
            logging.info(f'Made move {move}, response: {resp}')

    async def _get_game(self):
        async with self._session.get(f'{self._api_url}/game') as resp:
            return (await resp.json())['data']

    async def _play_game(self):
        self.minimax = Minimax(self._player_num)
        current_game_progress = await self._get_game()
        is_finished = current_game_progress['is_finished']
        is_started = current_game_progress['is_started']
        while is_started and not is_finished:
            logging.info(f"Move of {current_game_progress['whose_turn']}")

            if current_game_progress['last_move'] is not None and \
                    current_game_progress['last_move']['last_moves'] != self._last_move:
                last_move = current_game_progress['last_move']['last_moves']
                logging.info(f"Move from server: {last_move}")
                moves = []
                for m in last_move:
                    if m not in self._last_move:
                        moves.append(m)

                for move in moves:
                    self._game.move(move)
                self._last_move = moves

            if self._player['color'] == current_game_progress['whose_turn']:
                move = self.heuristic()
                logging.info(f"New move: {move}")
                await self._make_move(move)

            current_game_progress = await self._get_game()
            is_finished = current_game_progress['is_finished']
            is_started = current_game_progress['is_started']

            await asyncio.sleep(0.1)

    async def start(self):
        logging.info('API Tester initialized, test will start in 2 secs')

        await self._prepare_player(self._player_num)

        logging.info('Game started, players initialized')

        logging.info(f'Players: {self._player}')

        await asyncio.sleep(0.5)

        await self._play_game()

        logging.info('Game finished')
        last_game_progress = await self._get_game()
        logging.info(str(last_game_progress))

        await self._session.close()

    def heuristic(self):
        is_red = self._player['color'] == "RED"
        print('is_red')
        print(is_red)
        print('/is_res')
        return self.minimax.make_best_move(1 if is_red else 2, self._game.board) if is_red else random.choice(
            self._game.get_possible_moves())


async def start_bot(player_name):
    loop = asyncio.get_event_loop()
    player = ApiTester(loop, player_name)
    await player.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if sys.argv.__len__() > 1 and sys.argv[1]:
        loop.run_until_complete(start_bot(sys.argv[1]))
    else:
        loop.run_until_complete(start_bot("BUBILDA"))

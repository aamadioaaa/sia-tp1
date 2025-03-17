from src.sokoban import Sokoban

basic_grid = """
#######
#@    #
#     #
#     #
#     #
#######
"""

def test_movements():
   s = Sokoban()
   s.parse_grid(basic_grid)
   assert s.player == (2, 1)
   assert s.move_up() is None
   assert s.move_left() is None
   s = s.move_right()
   s = s.move_down()
   assert s.player == (3, 2)


basic_grid_with_boxes = """
#######
#@$   #
# $   #
#     #
#     #
#######
"""

def test_boxes():
   s = Sokoban()
   s.parse_grid(basic_grid_with_boxes)
   assert s.player == (2, 1)
   assert s.boxes == [(2, 2), (3, 2)]
   s = s.move_right()
   s = s.move_down()
   assert s.player == (3, 2)
   assert s.boxes == [(2, 3), (4, 2)]
   assert (s.grid == "$").sum() == 2
   assert (s.grid == "@").sum() == 1


basic_grid_with_objective = """
#######
#@$  .#
#   $ #
#   . #
#     #
#######
"""
def test_is_finished():
   s = Sokoban()
   s.parse_grid(basic_grid_with_objective)
   for _ in range(2):
      s = s.move_right()
      assert not s.is_finished()
   s = s.move_right()
   s = s.move_down()
   assert s.is_finished()


basic_grid_without_deadlock = """
#######
#@$  .#
#   $ #
#   . #
#     #
#######
"""
def test_is_not_deadlocked():
   s = Sokoban()
   s.parse_grid(basic_grid_without_deadlock)
   for _ in range(2):
      s = s.move_right()
      assert not s.is_finished()
      assert not s.is_deadlocked()
   s = s.move_right()
   s = s.move_down()
   assert s.is_finished()
   assert not s.is_deadlocked()


basic_grid_with_deadlock = """
#######
#@$   #
#     #
#     #
#     #
#######
"""
def test_is_deadlocked():
   s = Sokoban()
   s.parse_grid(basic_grid_with_deadlock)
   for _ in range(2):
      s = s.move_right()
      assert not s.is_finished()
      assert not s.is_deadlocked()
   s = s.move_right()
   assert s.is_deadlocked()

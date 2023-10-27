# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import omni.ui as ui
from omni.ui import scene as sc
from omni.ui_scene._scene import AbstractGesture


def setcolor(sender, color):
    """
    Sets the color of the sender

    Args:
        `sender : omni.ui.scene.Manipulator`
            The shape driving the gesture
        `color : omni.ui.color`
            The color that will be assigned to the shape
    """
    sender.color = color


class Manager(sc.GestureManager):
    """
    The object that controls batch processing and preventing of gestures.
    See more here: https://docs.omniverse.nvidia.com/kit/docs/omni.ui.scene/latest/omni.ui.scene/omni.ui.scene.GestureManager.html
    """

    def should_prevent(self, gesture: AbstractGesture, preventer: AbstractGesture) -> bool:
        """
        Called per gesture. Determines if the gesture should be prevented with another gesture. 
        Useful to resolve intersections.

        Args:
            `gesture : AbstractGesture`
                Gesture that is occurring
            `preventer : AbstractGesture`
                Gesture preventing `gesture`

        Returns:
            bool: Whether or not the gesture should be prevented. 
            If True gesture will be prevented otherwise the gesture will overtake the last gesture used.
        """
        if gesture.name == "SelectionDrag" and preventer.state == sc.GestureState.BEGAN:
            return True
        if gesture.name == "SelectionClick" and preventer.name == "color_change":
            return True


class Move(sc.DragGesture):
    """
    Inherits from `DragGesture`, the gesture that provides a way to capture click-and-drag mouse event.
    See more here: https://docs.omniverse.nvidia.com/kit/docs/omni.ui.scene/latest/omni.ui.scene/omni.ui.scene.DragGesture.html
    """

    def __init__(self, transform: sc.Transform, **kwargs):
        """
        Construct the gesture to track mouse drags

        Args:
            `transform : sc.Transform` The transform parent of the shape.

            `kwargs : dict`
                See below

        ### Keyword Arguments:

            `mouse_button : `
                Mouse button that should be active to start the gesture.

            `modifiers : `
                The keyboard modifier that should be active ti start the gesture.

            `check_mouse_moved : `
                The check_mouse_moved property is a boolean flag that determines whether the DragGesture should verify if the 2D screen position of the mouse has changed before invoking the on_changed method. This property is essential in a 3D environment, as changes in the camera position can result in the mouse pointing to different locations in the 3D world even when the 2D screen position remains unchanged.

        Usage
        When check_mouse_moved is set to True, the DragGesture will only call the on_changed method if the actual 2D screen position of the mouse has changed. This can be useful when you want to ensure that the on_changed method is only triggered when there is a genuine change in the mouse's 2D screen position.
        If check_mouse_moved is set to False, the DragGesture will not check for changes in the mouse's 2D screen position before calling the on_changed method. This can be useful when you want the on_changed method to be invoked even if the mouse's 2D screen position hasn't changed, such as when the camera position is altered, and the mouse now points to a different location in the 3D world.

            `on_began_fn : `
                Called if the callback is not set when the user clicks the mouse button.

            `on_changed_fn : `
                Called if the callback is not set when the user moves the clicked button.

            `on_ended_fn : `
                Called if the callback is not set when the user releases the mouse button.

            `name : `
                The name of the object. It's used for debugging.

            `manager : `
                The Manager that controld this gesture.
        """
        super().__init__(**kwargs)
        self.__transform = transform

    def on_changed(self):
        """
        Called when the user moves the clicked button. Moves the sender in the direction the mouse was moved.
        """
        translate = self.sender.gesture_payload.moved
        # Move transform to the direction mouse moved
        current = sc.Matrix44.get_translation_matrix(*translate)
        self.__transform.transform *= current


manager = Manager()


class LineManipulator(sc.Manipulator):
    """
    Class that holds a custom Manipulator. Inherits from omni.ui.scene.Manipulator class.
    See more here: https://docs.omniverse.nvidia.com/kit/docs/omni.ui.scene/latest/omni.ui.scene/omni.ui.scene.Manipulator.html
    """

    def __init__(self, desc: dict, **kwargs) -> None:
        """
        ### Arguments:
            `desc : dict`
                Description of the manipulator

            `kwargs : dict`
                See below

        ### Keyword Arguments:

            `gestures : `
                All the gestures assigned to this shape.

            `model : `
                The model of the class.
        """
        super().__init__(**kwargs)

    def on_build(self) -> None:
        """
        Builds the Scene UI.
        Consists of a beige line that stretches in the X-axis.
        Called when Manipulator is dirty to build the content. It's another way to build the manipulator's content on the case the user doesn't want to reimplement the class.
        """
        transform = sc.Transform()
        with transform:
            sc.Line(
                [-50, 0, 0],
                [50, 0, 0],
                color=ui.color.beige,
                thickness=10,
                gestures=[
                    sc.ClickGesture(
                        lambda s: setcolor(s, ui.color.green), mouse_button=0, name="color_change", manager=manager
                    ),
                    sc.DoubleClickGesture(
                        lambda s: setcolor(s, ui.color.beige), mouse_button=0, name="color_change", manager=manager
                    ),
                    Move(transform, manager=manager),
                ],
            )
            with sc.Transform(transform=sc.Matrix44.get_translation_matrix(0, 20, 0)):
                sc.Label(
                    "Click and Drag the Line to Move me\nClick or Double Click to Change color",
                    size=18,
                    alignment=ui.Alignment.CENTER,
                    color=ui.color.blue,
                )

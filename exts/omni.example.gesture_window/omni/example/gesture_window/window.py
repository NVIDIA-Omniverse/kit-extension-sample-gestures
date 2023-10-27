# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import omni.ui as ui
from omni.ui import scene as sc
from omni.ui_scene._scene import AbstractGesture

proj = [0.5, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 2e-7, 0, 0, 0, 1, 1]


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
        if gesture.name != "gesture_name" and preventer.state == sc.GestureState.BEGAN:
            return True


manager = Manager()


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


class GestureWindowExample(ui.Window):
    """
    omni.ui.Window that hold two Rectangles
    Both Rectangles can be hovered, clicked, and dragged
    As each gesture is being used the label in the middle of the window will update with the current gesture being used.
    See more here: https://docs.omniverse.nvidia.com/kit/docs/omni.ui/latest/omni.ui/omni.ui.Window.html
    """

    def __init__(self, title: str, **kwargs) -> None:
        """
        Construct the window, add it to the underlying windowing system, and makes it appear.

        ### Arguments:

            `title :`
                The window title. It's also used as an internal window ID.

            `kwargs : dict`
                See below

        ### Keyword Arguments:

            `flags : `
                This property set the Flags for the Window.

            `visible : `
                This property holds whether the window is visible.

            `title : `
                This property holds the window's title.

            `padding_x : `
                This property set the padding to the frame on the X axis.

            `padding_y : `
                This property set the padding to the frame on the Y axis.

            `width : `
                This property holds the window Width.

            `height : `
                This property holds the window Height.

            `position_x : `
                This property set/get the position of the window in the X Axis. The default is kWindowFloatInvalid because we send the window position to the underlying system only if the position is explicitly set by the user. Otherwise the underlying system decides the position.

            `position_y : `
                This property set/get the position of the window in the Y Axis. The default is kWindowFloatInvalid because we send the window position to the underlying system only if the position is explicitly set by the user. Otherwise the underlying system decides the position.

            `auto_resize : `
                setup the window to resize automatically based on its content

            `noTabBar : `
                setup the visibility of the TabBar Handle, this is the small triangle at the corner of the view If it is not shown then it is not possible to undock that window and it need to be closed/moved programatically

            `raster_policy : `
                Determine how the content of the window should be rastered.

            `width_changed_fn : `
                This property holds the window Width.

            `height_changed_fn : `
                This property holds the window Height.

            `visibility_changed_fn : `
                This property holds whether the window is visible.
        """
        super().__init__(title, **kwargs)
        self.label = None
        self.frame.set_build_fn(self._build_fn)

    def _build_fn(self):
        """
        The callback that will be called once the frame is visible and the content of the callback will override the frame child. It's useful for lazy load.
        """
        with self.frame:
            with ui.VStack():
                self.label = ui.Label("Sender: None\nAction: None", alignment=ui.Alignment.CENTER, size=16)
                scene_view = sc.SceneView(
                    sc.CameraModel(proj, 1), aspect_ratio_policy=sc.AspectRatioPolicy.PRESERVE_ASPECT_FIT
                )
                with scene_view.scene:
                    transform = sc.Transform()
                    with transform:
                        sc.Rectangle(
                            2,
                            2,
                            color=ui.color.beige,
                            thickness=5,
                            gestures=[
                                sc.ClickGesture(
                                    lambda s: setcolor(s, ui.color.blue), manager=manager, name="gesture_name"
                                ),
                                sc.DoubleClickGesture(
                                    lambda s: setcolor(s, ui.color.beige), manager=manager, name="gesture_name"
                                ),
                                Move(transform, manager=manager, name="gesture_name"),
                                sc.HoverGesture(
                                    on_began_fn=lambda s: setcolor(s, ui.color.black),
                                    on_changed_fn=lambda s: self.print_action(s, "Hover Changed"),
                                    on_ended_fn=lambda s: self.print_action(s, "Hover End"),
                                ),
                            ],
                        )
                    transform = sc.Transform(transform=sc.Matrix44.get_translation_matrix(0, 0, -1))
                    with transform:
                        sc.Rectangle(
                            2,
                            2,
                            color=ui.color.olive,
                            thickness=5,
                            gestures=[
                                sc.ClickGesture(lambda s: setcolor(s, ui.color.red)),
                                sc.DoubleClickGesture(lambda s: setcolor(s, ui.color.olive)),
                                Move(transform),
                                sc.HoverGesture(
                                    on_began_fn=lambda s: setcolor(s, ui.color.black),
                                    on_changed_fn=lambda s: self.print_action(s, "Hover Changed"),
                                    on_ended_fn=lambda s: self.print_action(s, "Hover End"),
                                ),
                            ],
                        )

    def print_action(self, sender, action):
        """
        Prints the action / gesture to the label in the middle of the window

        Args:
            sender : Where the gesture is coming from
            action : The type of gesture being used
        """
        self.label.text = f"Sender: {sender}\nAction: {action}"

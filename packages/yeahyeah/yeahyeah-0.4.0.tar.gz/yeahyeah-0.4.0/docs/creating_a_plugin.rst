=================
Creating a plugin
=================

<TODO: expand this into an actual tutorial. For now just pointers>

To create a plugin for yeahyeah, do the following:


* Create the following package structure::

    -<yourplugin_plugin>
        |-cli.py
        |-core.py


* In `core.py`, subclass YeahYeahPlugin::

    class YourPlugin(YeahYeahPlugin):

    slug = "my_plugin"
    short_slug = "my"

    def get_commands(self):
        """

        Returns
        -------
        List[click.Command]
            A list of click commands or groups to
            add to the yeahyeah main menu
        """
        raise NotImplemented()


    def get_admin_commands(self):
        """

        Returns
        -------
        List[click.Command]
            list of click commands that can be used
            to admin this plugin

        """
        raise NotImplemented()

* If you want to access the settings directory during plugin initialization, overwrite the `init_from_context(cls, context: YeahYeahContext)` method


* If you want to pass your own context (paths, objects, passwords?) to your plugin's methods, put this in `cli.py`::

    class MyContext:
        def __init__(foo)
            self.foo = foo

    #
    @click.group(name='myplugin')
    @click.pass_context
    def main(ctx: YeahYeahContext):
            """Yourplugin description"""
            ctx.obj = yeahyeah_context
            #  read whatever fields you need from yeahyeah_context,
            #  and replace with your own context
            ctx.obj = MyContext(foo='baz')

    #  this creates a decorator that will return the closest
    #  MyContext object in the call hierarchy
    pass_my_context = click.make_pass_decorator(MyContext)

    @click.command()
    @pass_my_context
    def a_method(context: MyContext):
        click.echo(f"My context value was {context.foo}")



* To include your plugin in yeahyeah, edit yeahyeah.cli.py and add you plugin

<TODO: Create proper mechanism for including plugins without editing source code. Would be nice..>

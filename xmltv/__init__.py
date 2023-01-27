from datetime import datetime


class Channel:
    def __init__(
            self,
            channel_id: str,
            display_name: str,
            programme_title: str,
            programme_start: datetime,
            programme_stop: datetime
    ):
        self.channel_id = channel_id
        self.display_name = display_name
        self.programme_title = programme_title
        self.programme_start = programme_start
        self.programme_stop = programme_stop


class Xmltv:
    def __init__(self, channels: list[Channel]):
        self.channels = channels

    def generate_text(self) -> str:
        xmltv_text = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
        xmltv_text += "<tv>\n"

        for channel in self.channels:
            xmltv_text += f"    <channel id=\"{channel.channel_id}\">\n"
            xmltv_text += f"        <display-name lang=\"zh\">{channel.display_name}</display-name>\n"
            xmltv_text += "    </channel>\n"

            programme_start_str = channel.programme_start.strftime(
                "%Y%m%d%H%M") + "00 +0800"
            programme_stop_str = channel.programme_stop.strftime(
                "%Y%m%d%H%M") + "00 +0800"

            xmltv_text += f"    <programme start=\"{programme_start_str}\" " +\
                f"stop=\"{programme_stop_str}\" " +\
                f"channel=\"{channel.channel_id}\">\n"

            xmltv_text += f"        <title lang=\"zh\">{channel.programme_title}</title>\n"
            xmltv_text += f"        <desc lang=\"zh\">{channel.programme_title}</desc>\n"
            xmltv_text += "    </programme>\n"

        xmltv_text += "</tv>\n"

        return xmltv_text

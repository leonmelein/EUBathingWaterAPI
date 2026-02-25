<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Output MUST be XML for pandas.read_xml -->
    <xsl:output method="xml" indent="yes" encoding="UTF-8" />
    <xsl:strip-space elements="*" />

    <xsl:template match="/">
        <rows>
            <!-- Adjust path if your XML wraps sites differently -->
            <xsl:for-each select="//supluskoht">

                <!-- If there are coordinates: emit one row per koordinaat -->
                <xsl:choose>
                    <xsl:when test="koordinaadid/koordinaat">
                        <xsl:for-each select="koordinaadid/koordinaat">
                            <row>
                                <id>
                                    <xsl:value-of select="../../id" />
                                </id>
                                <name>
                                    <xsl:value-of select="../../nimetus" />
                                </name>
                                <x>
                                    <xsl:value-of select="x" />
                                </x>
                                <y>
                                    <xsl:value-of select="y" />
                                </y>
                            </row>
                        </xsl:for-each>
                    </xsl:when>

                    <!-- No coordinates: still emit a row -->
                    <xsl:otherwise>
                        <row>
                            <id>
                                <xsl:value-of select="id" />
                            </id>
                            <name>
                                <xsl:value-of select="nimetus" />
                            </name>
                            <x />
                            <y />
                        </row>
                    </xsl:otherwise>
                </xsl:choose>

            </xsl:for-each>
        </rows>
    </xsl:template>

</xsl:stylesheet>
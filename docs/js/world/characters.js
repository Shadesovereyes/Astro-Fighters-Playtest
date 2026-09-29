/* Astro Fighters — approved paper-doll registry.
   Source authority: the committed /Paperdolls sheets (512×64, eight 64×64 directional frames).
   Runtime copies under docs/assets/characters/ are byte-identical (tools/validate-world-data.mjs).
   Frame order confirmed from the sheets: S, SE, E, NE, N, NW, W, SW (frames are never moved).
   Skin tones: tone0 Fair and tone3 Umber are palette swaps of tone1/tone2 made by
   tools/derive-skin-tones.mjs (same pixels and alpha, skin ramp recoloured).
   Draw order per frame: contact shadow → body → clothing → arms → shoulders → hair → eyes.
   Never register a redrawn, regenerated, resized, or resampled copy of any sheet. */
(() => {
  'use strict';
  window.AF_CHARACTERS = {
    frameOrder: ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW'],
    drawOrder: ['shadow', 'body', 'clothing', 'arms', 'shoulders', 'hair', 'eyes'],
    // Shared by every actor: 512×64, eight 64×64 frames, drawn under the body on the same registration.
    contactShadow: {path: 'assets/characters/shadow/contact-shadow.png', source: 'Paperdolls/contact-shadow.png', derivation: 'copy'},
    starterOutfit: 'gi',
    sexes: {
      "male": {
        "skin": {
          "tone0": {
            "label": "Fair",
            "body": {
              "path": "assets/characters/male/body/tone0.png",
              "source": "Paperdolls/Male/Layer 1 - Base Body/Male Base Body0.png"
            },
            "arms": {
              "path": "assets/characters/male/arms/tone0.png",
              "source": "Paperdolls/Male/Layer 3 - Arms/Male Arms0.png"
            }
          },
          "tone1": {
            "label": "Light",
            "body": {
              "path": "assets/characters/male/body/tone1.png",
              "source": "Paperdolls/Male/Layer 1 - Base Body/Male Base Body1.png"
            },
            "arms": {
              "path": "assets/characters/male/arms/tone1.png",
              "source": "Paperdolls/Male/Layer 3 - Arms/Male Arms1.png"
            }
          },
          "tone2": {
            "label": "Deep",
            "body": {
              "path": "assets/characters/male/body/tone2.png",
              "source": "Paperdolls/Male/Layer 1 - Base Body/Male Base Body2.png"
            },
            "arms": {
              "path": "assets/characters/male/arms/tone2.png",
              "source": "Paperdolls/Male/Layer 3 - Arms/Male Arms2.png"
            }
          },
          "tone3": {
            "label": "Umber",
            "body": {
              "path": "assets/characters/male/body/tone3.png",
              "source": "Paperdolls/Male/Layer 1 - Base Body/Male Base Body3.png"
            },
            "arms": {
              "path": "assets/characters/male/arms/tone3.png",
              "source": "Paperdolls/Male/Layer 3 - Arms/Male Arms3.png"
            }
          }
        },
        "hair": {
          "afro": {
            "label": "Afro",
            "layer": {
              "path": "assets/characters/male/hair/afro.png",
              "source": "Paperdolls/Male/Layer 5 - Hair/Afro Hair.png"
            }
          },
          "fade": {
            "label": "Fade",
            "layer": {
              "path": "assets/characters/male/hair/fade.png",
              "source": "Paperdolls/Male/Layer 5 - Hair/Fade Hair.png"
            }
          },
          "long": {
            "label": "Long",
            "layer": {
              "path": "assets/characters/male/hair/long.png",
              "source": "Paperdolls/Male/Layer 5 - Hair/Long Hair.png"
            }
          }
        },
        "eyes": {
          "brown": {
            "label": "Brown",
            "layer": {
              "path": "assets/characters/male/eyes/brown.png",
              "source": "Paperdolls/Male/Layer 6 - Eyes/Brown Eyes.png"
            }
          },
          "purple": {
            "label": "Purple",
            "layer": {
              "path": "assets/characters/male/eyes/purple.png",
              "source": "Paperdolls/Male/Layer 6 - Eyes/Purple Eyes.png"
            }
          }
        },
        "outfits": {
          "gi": {
            "label": "Gi",
            "clothing": {
              "path": "assets/characters/male/clothing/gi.png",
              "source": "Paperdolls/Male/Layer 2 - Clothing/Male Gi.png"
            }
          },
          "red-armor": {
            "label": "Red Armor",
            "clothing": {
              "path": "assets/characters/male/clothing/red-armor.png",
              "source": "Paperdolls/Male/Layer 2 - Clothing/Male Red Armor.png"
            },
            "shoulders": {
              "path": "assets/characters/male/shoulders/red-armor.png",
              "source": "Paperdolls/Male/Layer 4 - Shoulders and Arms accessories/Red Armor Shoulders.png"
            }
          },
          "blue-armor": {
            "label": "Blue Armor",
            "clothing": {
              "path": "assets/characters/male/clothing/blue-armor.png",
              "source": "Paperdolls/Male/Layer 2 - Clothing/Male Blue Armor.png"
            },
            "shoulders": {
              "path": "assets/characters/male/shoulders/blue-armor.png",
              "source": "Paperdolls/Male/Layer 4 - Shoulders and Arms accessories/Blue Armor Shoulders.png"
            }
          }
        }
      },
      "female": {
        "skin": {
          "tone0": {
            "label": "Fair",
            "body": {
              "path": "assets/characters/female/body/tone0.png",
              "source": "Paperdolls/Female/Layer 1 - Base Body/Female Base Body0.png"
            },
            "arms": {
              "path": "assets/characters/female/arms/tone0.png",
              "source": "Paperdolls/Female/Layer 3 - Arms/Female Arms0.png"
            }
          },
          "tone1": {
            "label": "Light",
            "body": {
              "path": "assets/characters/female/body/tone1.png",
              "source": "Paperdolls/Female/Layer 1 - Base Body/Female Base Body1.png"
            },
            "arms": {
              "path": "assets/characters/female/arms/tone1.png",
              "source": "Paperdolls/Female/Layer 3 - Arms/Female Arms1.png"
            }
          },
          "tone2": {
            "label": "Deep",
            "body": {
              "path": "assets/characters/female/body/tone2.png",
              "source": "Paperdolls/Female/Layer 1 - Base Body/Female Base Body2.png"
            },
            "arms": {
              "path": "assets/characters/female/arms/tone2.png",
              "source": "Paperdolls/Female/Layer 3 - Arms/Female Arms2.png"
            }
          },
          "tone3": {
            "label": "Umber",
            "body": {
              "path": "assets/characters/female/body/tone3.png",
              "source": "Paperdolls/Female/Layer 1 - Base Body/Female Base Body3.png"
            },
            "arms": {
              "path": "assets/characters/female/arms/tone3.png",
              "source": "Paperdolls/Female/Layer 3 - Arms/Female Arms3.png"
            }
          }
        },
        "hair": {
          "afro": {
            "label": "Afro",
            "layer": {
              "path": "assets/characters/female/hair/afro.png",
              "source": "Paperdolls/Female/Layer 4 - Hair/Afro Hair.png"
            }
          },
          "long": {
            "label": "Long",
            "layer": {
              "path": "assets/characters/female/hair/long.png",
              "source": "Paperdolls/Female/Layer 4 - Hair/Long Hair.png"
            }
          }
        },
        "eyes": {
          "brown": {
            "label": "Brown",
            "layer": {
              "path": "assets/characters/female/eyes/brown.png",
              "source": "Paperdolls/Female/Layer 5 - Eyes/Brown Eyes.png"
            }
          },
          "purple": {
            "label": "Purple",
            "layer": {
              "path": "assets/characters/female/eyes/purple.png",
              "source": "Paperdolls/Female/Layer 5 - Eyes/Purple Eyes.png"
            }
          }
        },
        "outfits": {
          "gi": {
            "label": "Gi",
            "clothing": {
              "path": "assets/characters/female/clothing/gi.png",
              "source": "Paperdolls/Female/Layer 2 - Clothing/Female Gi.png"
            }
          }
        }
      }
    }
  };
})();

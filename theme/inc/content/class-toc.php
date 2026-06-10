<?php
namespace CD\Content;
class Toc {

	private $content;
	public $count;
	private $title;
	private $level;
	private $text;

	/**
	 * @param string $content A post includes the headers.
	 */
	public function __construct( $content = '' ) {
		global $post;
		if ( is_object( $post ) ) {
			if ( empty( $content ) ) {
				$content = $post->post_content;
			}
			// echo '<pre>' . print_r( esc_html( $content ), true ) . '<pre>'; die;
			preg_match_all( "/<h(2)[^>]+>(.*)<\/h(2)+>/i", $content, $match );
			if ( empty( $match[0] ) && empty( $match[1] ) && empty( $match[2] ) ) {
				preg_match_all( "#<[hH](2)>(.*?)</[hH](2)>#is", $content, $match );
			}
			$this->content = $content;
			$this->count   = count( $match[0] );
			$this->title   = $match[0];
			$this->level   = $match[1];
			$this->text    = $match[2];
		}
	}


	/**
	 * Creates an array of table of contents data structure.
	 *
	 * @return array
	 */
	public function getDataToc() {
		$toc = [];

		$count = $this->count;
		$level = $this->level;
		$text  = $this->text;
		for ( $i = 0, $j = 0; $i < $count; $i ++, $j ++ ) {
			// the first header
			if ( $i === 0 ) {
				$toc[ $i ]['list_open']  = true;
				$toc[ $i ]['item_open']  = true;
				$toc[ $i ]['text']       = $text[ $i ];
				$toc[ $i ]['href']       = $this->getHref( $i );
				$toc[ $i ]['item_close'] = true;
				$toc[ $i ]['list_close'] = false;
				$toc[ $i ]['level']      = $level[ $i ];

				continue;
			}

			// the last header
			if ( $i === $count - 1 ) {
				$toc[ $i ]['list_open'] = $level[ $i ] > $level[ $i - 1 ];;
				$toc[ $i ]['item_open']  = true;
				$toc[ $j ]['text']       = $text[ $i ];
				$toc[ $j ]['href']       = $this->getHref( $i );
				$toc[ $i ]['item_close'] = true;
				$toc[ $i ]['list_close'] = true;
				$toc[ $i ]['level']      = $level[ $i ];
				$j ++;
				break;
			}

			$toc[ $j ]['list_open']  = $level[ $i ] > $level[ $i - 1 ];
			$toc[ $j ]['item_open']  = true;
			$toc[ $j ]['text']       = $text[ $i ];
			$toc[ $j ]['href']       = $this->getHref( $i );
			$toc[ $j ]['item_close'] = $level[ $i ] >= $level[ $i + 1 ];
			$toc[ $j ]['list_close'] = $level[ $i ] > $level[ $i + 1 ];
			$toc[ $j ]['level']      = $level[ $i ];

		}

		return $toc;
	}

	/**
	 * Adds Href tag to H2
	 *
	 * @return string
	 */
	public function getPostMarkup() {

		$content = $this->content;
		$count   = $this->count;
		$title   = $this->title;
		$level   = $this->level;


		for ( $i = 0; $i < $count; $i ++ ) {
			$pattern     = '/<h' . $level[$i] . '([^>]*)>/';
			$replacement = '<h' . $level[$i] . '$1 id="toc_' . $i . '">';
			
			//Add Toc Id to Header
			$new_title = preg_replace( $pattern,
				$replacement,
				$title[ $i ]
			);

//			Replace entire heading
			$content = str_replace( $title[ $i ],
				$new_title,
				$content );
		}

		return $content;
	}


	/**
	 * Generates table of contents.
	 * 
	 * @param bool $is_widget_area If this will be rendered in widget area.
	 *
	 * @return string
	 */
	public function getToc( $is_widget_area = false ) {
		// $active  = ! wp_is_mobile() ? 'active' : '';
		$active = '';
		$dataToc = $this->getDataToc();
		$toc     = '';
		$toc     .= '<div class="toc">';
		$toc     .= '<div class="toc__pill">Contents</div>';
		foreach ( $dataToc as $item ) {
			if ( $item['item_close'] ) {
				$toc .= '</li>';
			}
			if ( $item['list_open'] ) {
				$toc .= '<ol>';
			}
			if ( $item['item_open'] ) {
				$toc .= '<li>';
			}
			if ( $item['text'] ) {
				$toc .= '<a href="' . $item['href'] . '"' . ' class="toc__li"' . '>' . $item['text'] . '</a>';
			}
			if ( $item['list_close'] ) {
				$toc .= '</ol>';
			}
		}
		$toc .= '</div>';

		if ( ! $is_widget_area ) {
			$toc .= $this->title[0];
		}
		
		return $toc;
	}


	/**
	 * Get a modified post with a content marked up for  table of contents.
	 *
	 * @return string
	 */
	public function getPostTocInContent() {
		$toc                        = $this->getToc();
		$first_h2                   = $this->title[0];
		
		$content_with_toc           = str_replace( $first_h2,
			$toc,
			$this->content
		);
		$this->content              = $content_with_toc;
		$marked_up_content_with_toc = $this->getPostMarkup();

		return $marked_up_content_with_toc;
	}

	/**
	 * Added for the desktop version with no sidebar.
	 * @return string
	 */
	public function getPostTocInContentNoToC() {
		$marked_up_content_with_toc = $this->getPostMarkup();

		return $marked_up_content_with_toc;
	}


	/**
	 * @access protected
	 * @return string
	 */
	protected function getHref( $str ) {
		return "#" . 'toc_' . $str;
	}
}
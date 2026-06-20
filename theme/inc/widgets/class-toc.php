<?php

namespace CD\Widgets;

class Toc {

	private $content;
	public $count;
	private $title;
	private $level;
	private $text;

	/**
	 * @param string $content A post includes the headers.
	 */
	public function __construct( $content ) {
		preg_match_all( "#<[hH]([2])(.*?)>(.*?)</[hH][2]>#is", $content, $match );
		
		$this->content = $content;
		$this->count   = count( $match[0] );
		$this->title   = $match[0];
		$this->level   = $match[1];
		$this->text    = $match[3];
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
				$toc[ $i ]['list_open'] = true;
				$toc[ $i ]['item_open'] = true;
				$toc[ $i ]['text']      = $text[ $i ];
				$toc[ $i ]['href']      = $this->getHref(  $i  );
				$toc[ $i ]['item_close'] = $level[ $i ] == $level[ $i + 1 ] or ( ! isset( $level[ $i + 1 ] ) );
				$toc[ $i ]['list_close'] = $level[ $i ] > $level[ $i + 1 ] or ( ! isset( $level[ $i + 1 ] ) );

				continue;
			}

			// the last header
			if ( $i == $count - 1 ) {
				$toc[ $j ]['list_open']  = $level[ $i ] > $level[ $i - 1 ];
				$toc[ $j ]['item_open']  = true;
				$toc[ $j ]['text']       = $text[ $i ];
				$toc[ $j ]['href']       = $this->getHref(  $i  );
				$toc[ $j ]['item_close'] = true;
				$toc[ $j ]['list_close'] = $level[ $i ] > $level[ $i - 1 ];

				++ $j;
				$toc[ $j ]['list_open']  = false;
				$toc[ $j ]['item_open']  = false;
				$toc[ $j ]['text']       = "";
				$toc[ $j ]['href']       = "";
				$toc[ $j ]['item_close'] = true;
				$toc[ $j ]['list_close'] = true;

				break;
			}

			//other header
			$toc[ $j ]['list_open']  = $level[ $i ] > $level[ $i - 1 ];
			$toc[ $j ]['item_open']  = true;
			$toc[ $j ]['text']       = $text[ $i ];
			$toc[ $j ]['href']       = $this->getHref(  $i  );
			$toc[ $j ]['item_close'] = $level[ $i ] >= $level[ $i + 1 ];
			$toc[ $j ]['list_close'] = $level[ $i ] > $level[ $i + 1 ];

			if ( $level[ $i ] > $level[ $i + 1 ] ) {
				++ $j;
				$toc[ $j ]['list_open']  = false;
				$toc[ $j ]['item_open']  = false;
				$toc[ $j ]['text']       = "";
				$toc[ $j ]['href']       = "";
				$toc[ $j ]['item_close'] = true;
				$toc[ $j ]['list_close'] = false;
			}
		}

		return $toc;
	}

	/**
	 * Get a modified post.
	 *
	 * @return string
	 */
	public function getPost() {

		$content = $this->content;
		$count   = $this->count;
		$title   = $this->title;


		for ( $i = 0; $i < $count; $i ++ ) {


			$new_title = str_replace('<h2>',
				'<h2 id="toc_' . $i . '">',
				$title[$i]
			);

			$content = str_replace( $title[ $i ],
				$new_title,
				$content );
		}
		return $content;
	}


	/**
	 * Get a generated table of contents.
	 *
	 * @return string
	 */
	public function getToc() {
		$dataToc = $this->getDataToc();
		foreach ( $dataToc as $item ) {
			if ( $item['list_open'] ) { ?>
				<ul class="toc__ul  active">
			<?php }
			if ( $item['item_open'] ) { ?>
				<li class="toc__li">
			<?php }
			if ( $item['text'] ) { ?>
				<a href="<?= $item['href'] ?>" title="<?= $item['text'] ?>"><?= $item['text'] ?></a>
			<?php }
			if ( $item['item_close'] ) { ?>
				</li>
			<?php }
			if ( $item['list_close'] ) { ?>
				</ul>
			<?php }
		}
		return $toc;
	}


	/**
	 * Get a modified post with a content marked up for  table of contents.
	 *
	 * @return string
	 */
	public function getPostTocMarkup() {
//		var_dump($this->getPost());
		return $this->getPost();
	}


	/**
	 * @access protected
	 * @return string
	 */
	protected function getHref( $str ) {

		return "#" . 'toc_' . $str ;
	}


	/**
	 * @access protected
	 * @return string
	 */
	protected function getTagId( $str ) {

		return str_replace( ' ', '_', $str );
	}
}



